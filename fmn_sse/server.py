# -*- coding: utf-8 -*-
# Copyright (C) 2017 Jeremy Cline
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

from __future__ import absolute_import, unicode_literals

from collections import namedtuple
from gettext import gettext as _
import json
import logging
import re

import fedmsg
import six
from pika import ConnectionParameters, exceptions as pika_exceptions
from pika.adapters import twisted_connection
from twisted.internet import reactor, defer, protocol, error
from twisted.web import server, resource


_log = logging.getLogger(__name__)
app_config = fedmsg.config.load_config()


# Create a few namedtuples to make the various tuples used throughout
# this module slightly clearer.
RabbitQueue = namedtuple(u'RabbitQueue', [u'queue', u'consumer_tag'])
SubscriptionEntry = namedtuple(u'SubscriptionEntry', [u'queue', u'requests'])


class SSEServer(resource.Resource):
    """
    A Twisted Server-Sent Event server that consumes its messages from RabbitMQ.

    There is only one endpoint for this server. Clients can request resources
    in the format ``/<RabbitMQ exchange>/<RabbitMQ queue>/``. An HTTP response
    with the SSE headers announcing it is an event stream are immediately
    returned. As messages are pushed to the RabbitMQ consumer, they are in turn
    pushed to all HTTP clients.

    The response is never closed from the server's side. It continues to push
    events until the client disconnects.
    """
    isLeaf = True

    def __init__(self, *args, **kwargs):
        resource.Resource.__init__(self, *args, **kwargs)
        self.expire_ms = int(app_config.get('fmn.sse.pika.msg_expiration', 3600000))
        self.amqp_host = app_config.get('fmn.sse.pika.host', 'localhost')
        self.amqp_port = int(app_config.get('fmn.sse.pika.port', 5672))
        self.amqp_parameters = ConnectionParameters(self.amqp_host, self.amqp_port)

        whitelist = app_config.get('fmn.sse.webserver.queue_whitelist')
        self.whitelist = re.compile(whitelist) if whitelist else None
        blacklist = app_config.get('fmn.sse.webserver.queue_blacklist')
        self.blacklist = re.compile(blacklist) if blacklist else None

        self.allow_origin = app_config.get('fmn.sse.webserver.allow_origin', '*')
        self.prefetch_count = app_config.get('fmn.sse.pika.prefetch_count',  5)
        self.connection = None
        self.channel = None

        # Maps queues to open requests. The datastructure is in the format
        # {
        #   '<queue_name>': {'queue': RabbitQueue, 'requests': []},
        # }
        self.subscribers = {}

    @defer.inlineCallbacks
    def queue(self, queue, queue_arguments=None):
        """
        Construct and retrieve a queue from RabbitMQ.

        This will declare the queue in RabbitMQ if it doesn't already exist.

        The queue returned is a subclass of twisted.internet.defer.DeferredQueue.
        Calling ``get`` on the queue returns a ``Deferred`` that fires with
        (channel, method, properties, body) where the types are
        (pika.Channel, pika.spec.Basic.Deliver, pika.spec.BasicProperties, bytes).

        Afterwards you can do channel.basic_ack(delivery_tag=method.delivery_tag)
        to acknowledge message reciept.

        :param queue:           The queue to declare, bind to the exchange,
                                and consume from.
        :type  queue:           unicode str
        :param queue_arguments: custom arguments for the queue's construction
        :type  queue_agrements: dict

        :return: A Deferred that fires with a tuple of the queue to consume
                 messages from and a consumer tag.
        :rtype: Deferred of (pika.ClosableDeferredQueue, unicode str)
        """
        # TODO Handle errors appropriately
        if not self.connection:
            cc = protocol.ClientCreator(
                reactor,
                twisted_connection.TwistedProtocolConnection,
                self.amqp_parameters,
            )
            tcp_connection = yield cc.connectTCP(self.amqp_host, self.amqp_port)
            self.connection = yield tcp_connection.ready
        if not self.channel:
            self.channel = yield self.connection.channel()

        # TODO Consider using ``passive=True`` on ``exchange_declare`` and
        # ``queue_declare``. This causes an error if the queue or exchange don't
        # already exist, which we could then turn into a HTTP 404. Allowing
        # requests to cause exchanges or queues to be created seems like an easy
        # DoS attack.
        yield self.channel.queue_declare(
            queue=queue,
            durable=True,
            auto_delete=False,
            arguments={'x-message-ttl': self.expire_ms}
        )
        yield self.channel.basic_qos(prefetch_count=self.prefetch_count)
        deferred_queue, consumer_tag = yield self.channel.basic_consume(
            queue=queue,
            no_ack=False,
            exclusive=False,
        )
        queue = RabbitQueue(queue=deferred_queue, consumer_tag=consumer_tag)
        defer.returnValue(queue)

    def render_GET(self, request):
        """
        Handle GET requests to this endpoint. Requests should be to
        ``/<queue.name>/``.
        """
        # If the request ended in a trailing / the final path section is ''.
        # This allows the trailing / on /<exchange>/<queue>/ to be optional.
        if request.postpath[-1] == '':
            request.postpath.pop()
        if len(request.postpath) != 1:
            response = JsonNotFound()
            return response.render(request)

        # Only serve queues that are on the whitelist and not on the blacklist.
        # This is to avoid serving private queues used by FMN to dispatch work
        # to clients.
        queue_name = request.postpath[0]
        if self.whitelist and not self.whitelist.match(queue_name):
            response = JsonForbidden()
            return response.render(request)
        if self.blacklist and self.blacklist.match(queue_name):
            response = JsonForbidden()
            return response.render(request)

        request.setHeader(u'Content-Type', u'text/event-stream; charset=utf-8')
        request.setHeader(u'Access-Control-Allow-Origin', self.allow_origin)

        # The queue the request subscribes to may be empty, and it may not have
        # anything in it for a long time. Calling ``request.write`` here
        # ensures the response headers are written to the client immediately.
        # TODO can't do this here, we need to check if Rabbit is alive and the
        # queue exists. If it doesn't we should 503/404 etc.
        request.write(b'')

        request.notifyFinish().addBoth(self.request_closed, request, queue_name)

        if queue_name not in self.subscribers:
            # This is the first request for a particular queue
            subscription = {'queue': None, 'requests': [request]}
            self.subscribers[queue_name] = subscription
            self.new_subscription(queue_name)
        else:
            self.subscribers[queue_name]['requests'].append(request)
        return server.NOT_DONE_YET

    def new_subscription(self, queue_name):
        """
        Subscribe to a RabbitMQ queue.

        An entry will be made in the ``self.subscribers`` dictionary using the
        ``queue_name`` provided as the dictionary key.

        :param queue_name: The name of the queue to bind the request to.
        :type  queue_name: str
        """
        @defer.inlineCallbacks
        def write_requests(rabbit_queue):
            """
            A callback attached to the Deferred from TwistedRabbitConsumer's
            ``queue`` method. This is called once the queue is create and is
            responsible for writing new messages to requests.

            :param rabbit_queue: A namedtuple containing the queue and consumer tag.
            :type  rabbit_queue: RabbitQueue
            """
            subscription = self.subscribers[queue_name]
            subscription['queue'] = rabbit_queue

            while True:
                try:
                    channel, method, properties, body = yield rabbit_queue.queue.get()
                    for request in subscription['requests']:
                        msg = u'data: ' + body.decode('utf-8') + u'\r\n\r\n'
                        request.write(msg.encode('utf-8'))
                    yield channel.basic_ack(delivery_tag=method.delivery_tag)
                except pika_exceptions.ConsumerCancelled:
                    _log.info(_('The server has cancelled the AMQP consumer for '
                                'the {0} queue').format(queue_name))
                    for request in subscription['requests']:
                        request.finish()
                    break

        deferred_queue = self.queue(queue_name)
        deferred_queue.addCallback(write_requests)
        deferred_queue.addErrback(self.queue_error_handler, queue_name)
        return deferred_queue

    def queue_error_handler(self, err, queue_name):
        """
        Handle possible errors that occur in ``self.queue``
        """
        _log.info(str(err))
        if isinstance(err.value, error.ConnectionRefusedError):
            # RabbitMQ is down or refusing connections for some other reason;
            # Perform cleanup.
            for request in self.subscribers[queue_name]['requests']:
                # TODO finish with 503
                request.finish()
        elif isinstance(err.value, pika_exceptions.ChannelClosed):
            # Return the reason the channel was closed, try to restart the channel
            for request in self.subscribers[queue_name]['requests']:
                request.finish()
        else:
            _log.warning('Unhandled error: ' + str(err))

    @defer.inlineCallbacks
    def request_closed(self, err, request, queue_name):
        """
        Remove a request from the map of queues to open requests.

        This is intended to be called when a request is finished or closed.
        It can be added to a request by using ``request.notifyFinish``.

        :param err:         unused
        :param queue_name:  The name of the queue the request is attached to in
                            self.subscribers
        :type  queue_name:  str
        :param request:     The request to remove from self.subscribers
        """
        _log.debug('Removing ' + str(request) + ' from ' + str(queue_name))
        subscriber = self.subscribers[queue_name]
        subscriber['requests'].remove(request)
        if len(subscriber['requests']) == 0 and subscriber['queue']:
            # We need to notify the AMQP server so it stops pushing messages
            subscription = subscriber['queue']
            yield self.channel.basic_cancel(consumer_tag=subscription.consumer_tag)
            subscription.queue.close(pika_exceptions.ConsumerCancelled())
            self.subscribers.pop(queue_name)


class JsonErrorPage(resource.ErrorPage):
    """
    A resource that optionally returns a JSON body with error details.
    """

    def render(self, request):
        """
        Render a response for the request and return the UTF-8-encoded body.

        :param request: The request to reponse to.
        :type  request: twisted.web.http.Request

        :return: The body of the HTTP response to the request
        :rtype:  bytes
        """
        request.setResponseCode(self.code, self.brief.encode('utf-8'))

        if self.detail and isinstance(self.detail, dict):
            request.setHeader(
                u'content-type'.encode('utf-8'),
                u'application/json; charset=utf-8'.encode('utf-8')
            )
            body = json.dumps(self.detail)
        else:
            request.setHeader(
                u'content-type'.encode('utf-8'),
                u'text/html; charset=utf-8'.encode('utf-8')
            )
            body = self.template % {
                u'code': self.code,
                u'brief': self.brief,
                u'detail': self.detail,
            }

        if isinstance(body, six.text_type):
            body = body.encode('utf-8')
        return body


class JsonNotFound(JsonErrorPage):
    """A class to render a 404 Not Found page in either HTML or JSON."""

    def __init__(self, detail=_(u'Resource not found')):
        JsonErrorPage.__init__(self, 404, _(u'Not Found'), detail)


class JsonForbidden(JsonErrorPage):
    """A class to render a 403 Forbidden page in either HTML or JSON."""

    def __init__(self, detail=_(u'You are not allowed to access this resource')):
        JsonErrorPage.__init__(self, 403, _(u'Forbidden'), detail)


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    site = server.Site(SSEServer())
    port = int(app_config.get('fmn.sse.webserver.tcp_port', 8080))
    reactor.listenTCP(port, site)
    reactor.run()
