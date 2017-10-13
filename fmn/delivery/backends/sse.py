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
from __future__ import absolute_import, unicode_literals

from gettext import gettext as _
import logging

import pika
import fedmsg.meta
from pika.adapters import twisted_connection
from twisted.internet import reactor, protocol, defer

from .base import BaseBackend


_log = logging.getLogger(__name__)


class SSEBackend(BaseBackend):
    """
    This backend is responsible for the creation of RabbitMQ exchanges and
    queues and the re-publication of messages for consumption by the Server-
    Sent Events server.

    Messages are pulled off the "backend" queue and passed to this class, which
    formats them appropriately and pushes them back onto the appropriate
    exchange.
    """
    __context_name__ = "sse"

    def __init__(self, config):
        super(SSEBackend, self).__init__(config)

        self.expire_ms = int(self.config.get('fmn.pika.msg_expiration', 3600000))
        self.amqp_host = self.config.get('fmn.pika.host', 'localhost')
        self.amqp_port = int(self.config.get('fmn.pika.port', 5672))
        self.amqp_parameters = pika.ConnectionParameters(self.amqp_host, self.amqp_port)
        cc = protocol.ClientCreator(
            reactor,
            twisted_connection.TwistedProtocolConnection,
            self.amqp_parameters,
        )
        self._deferred_connection = cc.connectTCP(self.amqp_host, self.amqp_port)
        self._deferred_connection.addCallback(lambda conn: conn.ready)
        self.connection = None
        self.channel = None

    @defer.inlineCallbacks
    def deliver(self, formatted_message, recipient, raw_fedmsg):
        """
        Deliver a message to the recipient.

        .. warning::
            Although the original fedmsg is provided, be very careful when making
            use of it. The format will change from message to message, and schema
            changes are common.

        Args:
            formatted_message (str): The formatted message that is ready for delivery
                to the user. It has been formatted according to the user's preferences.
            recipient (dict): The recipient of the message.
            raw_fedmsg (dict): The original fedmsg that was used to produce the formatted
                message.
        """
        user = recipient['user']
        # TODO figure out when it's a group message
        queue = 'user-' + user
        _log.debug(_('Handling a message for {user} via server-sent '
                     'events').format(user=user))

        if not self.connection:
            self.connection = yield self._deferred_connection
        if not self.channel:
            self.channel = yield self.connection.channel()
        yield self.channel.queue_declare(
                queue=queue, durable=True, auto_delete=False,
                arguments={'x-message-ttl': self.expire_ms})

        # TODO consider confirming message delivery and retrying
        # on failure
        yield self.channel.basic_publish(
            exchange='',  # Publish to the default exchange
            routing_key=queue,
            body=formatted_message,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def handle_batch(self, session, recipient, queued_messages):
        """
        Handle sending a set of one or more messages to one recipient.

        :param session:     The SQLAlchemy database session to use.
        :type  session:     sqlalchemy.orm.session.Session
        :param recipient:   The recipient of the messages and their settings.
                            This controls what RabbitMQ queue the message ends
                            up in.
        :type recipient:    dict
        :param queued_messages:         The messages to send to the user.
        :type  queued_messages:         dict
        """
        message = _('Batching {count} messages for delivery via server-sent'
                    ' events').format(count=len(queued_messages))
        _log.debug(message)
        messages = [m.message for m in queued_messages]
        # Squash some messages into one conglomerate message
        # https://github.com/fedora-infra/datagrepper/issues/132
        messages = fedmsg.meta.conglomerate(messages, **self.config)
        for message in messages:
            self.handle(session, recipient, message)

    def handle_confirmation(self, session, confirmation):
        """
        This is an unimplemented method required by the parent class.
        """
        pass
