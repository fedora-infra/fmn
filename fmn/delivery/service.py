# -*- coding: utf-8 -*-
#
# This file is part of the FMN project.
# Copyright (C) 2017 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""
The FMN message delivery service.

This service is a `Twisted`_ application which consumes messages from an AMQP queue. Those
messages are then delivered using a back-end such as email or IRC. Messages are sent to
the queue by :func:`fmn.tasks.find_recipients` and :func:`fmn.tasks.batch_messages`.

This service is intended to be run using ``twistd`` and a Twisted application (.tac) file.

.. _Twisted: https://twistedmatrix.com/
"""
from __future__ import absolute_import

import logging

from kombu import Connection, Queue
from kombu.mixins import ConsumerMixin
from twisted.application import service
from twisted.internet import threads, reactor, defer
import six

from fmn import config
from fmn.constants import BACKEND_QUEUE_PREFIX
from .backends import sse, irc, debug, mail

_log = logging.getLogger(__name__)


class Consumer(ConsumerMixin):
    """
    A Kombu Consumer that ferries messages from AMQP into the Twisted reactor thread
    via a blocking API.

    This is intended to be run in its own thread using Twisted's :func:`reactor.callInThread`
    API. It will then use the :func:`threads.blockingCallFromThread` API to deliver messages
    into the Twisted reactor thread.

    Args:
        delivery_service (DeliveryService): Instance of the Twisted delivery service to use when
            dispatching messages to be sent inside the Twisted reactor thread.
        queues (list): A list of queues to consume from.
    """

    def __init__(self, delivery_service, queues):
        self.delivery_service = delivery_service
        self.broker_url = config.app_conf['celery']['broker']
        self.connection = Connection(self.broker_url)
        if isinstance(queues, six.string_types):
            queues = [queues]
        self.queues = [Queue(q) for q in queues]

    def get_consumers(self, consumer_class, channel):
        """
        Get the list of Consumers this class uses.

        This is part of the :class:`kombu.mixins.ConsumerMixin` API.

        Args:
            consumer_class (class): The class to use when creating consumers.
            channel (kombu.Channel): Unused.
        """
        return [
            consumer_class(self.queues, callbacks=[self.on_message], accept=['json']),
        ]

    def stop(self):
        """
        Set the flag to stop the AMQP consumers.

        This does not block and its return does not mean the consumers have been stopped.
        """
        _log.info('Halting the Kombu consumer')
        self.should_stop = True

    def on_consume_ready(self, connection, channel, consumers, **kwargs):  # pragma: no cover
        """
        Implement the ConsumerMixin API.

        Args:
            connection (kombu.Connection): Unused.
            channel (kombu.Channel): Unused.
            consumers (list): List of :class:`kombu.Consumer`. Unused.
        """
        _log.info('AMQP consumer ready on the %r queues', self.queues)
        super(Consumer, self).on_consume_ready(connection, channel, consumers, **kwargs)

    def on_consume_end(self, connection, channel):  # pragma: no cover
        """
        Implement the ConsumerMixin API.

        Args:
            connection (kombu.Connection): Unused.
            channel (kombu.Channel): Unused.
        """
        _log.info('Successfully canceled the AMQP consumer')
        super(Consumer, self).on_consume_end(connection, channel)

    def on_message(self, body, message):
        """
        The callback for the Consumer, called when a message is received.

        As this consumer must run outside the reactor thread (since it uses blocking APIs)
        this simply uses the Twisted API to call the delivery service's message handler inside
        the reactor thread.

        Args:
            body (dict): The decoded message body.
            message (kombu.Message): The Kombu message object.
        """
        try:
            threads.blockingCallFromThread(reactor, self.delivery_service.handle_message, body)
            message.ack()
        except Exception as e:
            # Something unexpected is wrong with the delivery backend - requeue the message
            # so we try again later.
            _log.error('Message delivery failed: %r', e)
            message.requeue()


class DeliveryService(service.Service):
    """
    The Twisted Service that handles the message delivery for FMN.

    Messages should already be formatted and ready for delivery without further
    processing when placed in the "backends" queue which this service subscribes
    to. All code called here should be Twisted-compatible (e.g. care should be
    taken with threads, no calls should block, etc.).
    """

    def startService(self):
        """Implementation of the Service API, called when the service is being started."""
        if config.app_conf.get('fmn.backends.debug', False):
            _log.info('"fmn.backends.debug" is True, using the DebugBackend')
            self.backends = {
                'sse': debug.DebugBackend(config=config.app_conf),
                'email': debug.DebugBackend(config=config.app_conf),
                'irc': debug.DebugBackend(config=config.app_conf),
            }
        else:
            self.backends = {
                'sse': sse.SSEBackend(config=config.app_conf),
                'email': mail.EmailBackend(config=config.app_conf),
                'irc': irc.IRCBackend(config=config.app_conf),
            }
        # Prune any backends that aren't enabled
        for key, value in self.backends.items():
            if key not in config.app_conf['fmn.backends']:
                del self.backends[key]
        # Also, check that we don't have something enabled that's not explicit
        for key in config.app_conf['fmn.backends']:
            if key not in self.backends:
                raise ValueError("%r in fmn.backends (%r) is invalid" % (
                    key, config.app_conf['fmn.backends']))

        _log.info('Running the FMN delivery service with the %r backends', self.backends.keys())
        queues = [BACKEND_QUEUE_PREFIX + b for b in self.backends.keys()]
        self.consumer = Consumer(self, queues)
        reactor.callInThread(self.consumer.run)

    @defer.inlineCallbacks
    def handle_message(self, message):
        """
        Send the message using the appropriate messaging backend.

        This method is intended to be called inside the thread running the Twisted reactor.

        Args:
            message (dict): The decoded message.

        Raises:
            Exception: Any exception raised by a backend handler.
        """
        _log.debug('Handling %r from the Twisted reactor thread', message)
        try:
            context = message['context']
            recipient = message['recipient']
            # This could be a dict, or a list if it's a batch message
            fedmsg = message['fedmsg']
            formatted_message = message['formatted_message']
        except Exception:
            _log.exception('Received a malformed message, "%r", from the backend queue'
                           ', dropping message!', message)
            return

        try:
            backend = self.backends[context]
        except KeyError:
            _log.error('Delivery request to the "%s" backend failed because there is no '
                       'backend loaded with that name', context)
            return

        try:
            yield backend.deliver(formatted_message, recipient, fedmsg)
        except Exception:
            # Logging from outside the twisted thread won't provide the full traceback, so catch
            # it here, log it for the traceback, and raise it again.
            _log.exception('The "%s" backend raised an unexpected exception while trying to '
                           'deliver a notification to recipient "%r"', context, recipient)
            raise
        if isinstance(fedmsg, dict):
            _log.info('Successfully delivered message %s to %s via %s',
                      fedmsg.get('body', {}).get('msg_id', 'UNKNOWN_ID'),
                      recipient.get('user', 'UNKOWN_USER'), context)
        else:
            _log.info('Successfully delivered a batch of %r messages to %r via %r',
                      len(fedmsg), recipient.get('user', 'UNKOWN_USER'), context)

    def stopService(self):
        """Implementation of the Service API, called when the service is shutting down."""
        self.consumer.stop()
