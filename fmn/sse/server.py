from __future__ import absolute_import, unicode_literals
from collections import namedtuple
import json
import logging

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
RequestKey = namedtuple(u'RequestKey', [u'exchange', u'queue'])


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
        cc = protocol.ClientCreator(
            reactor,
            twisted_connection.TwistedProtocolConnection,
            self.amqp_parameters,
        )
        self._deferred_connection = cc.connectTCP(self.amqp_host, self.amqp_port)
        self._deferred_connection.addCallback(lambda conn: conn.ready)
        self.connection = None
        self.channel = None

        # Maps queues to open requests. The datastructure is in the format
        # {
        #   RequestKey: {'queue': RabbitQueue, 'requests': []},
        # }
        self.subscribers = {}

    @defer.inlineCallbacks
    def queue(self, exchange=None, queue=None, routing_key=None,
              queue_arguments=None):
        """
        Construct and retrieve a queue from RabbitMQ.

        This will declare the exchange and queue in RabbitMQ if they don't
        already exist.

        The queue returned is a subclass of twisted.internet.defer.DeferredQueue.
        Calling ``get`` on the queue returns a ``Deferred`` that fires with
        (channel, method, properties, body) where the types are
        (pika.Channel, pika.spec.Basic.Deliver, pika.spec.BasicProperties, bytes).

        Afterwards you can do channel.basic_ack(delivery_tag=method.delivery_tag)
        to acknowledge message reciept.

        :param exchange:        The exchange to declare and bind the queue to.
        :type  exchange:        unicode str
        :param queue:           The queue to declare, bind to the exchange,
                                and consume from.
        :type  queue:           unicode str
        :param routing_key:     The queue routing key.
        :type  routing_key:     unicode str
        :param queue_arguments: custom arguments for the queue's construction
        :type  queue_agrements: dict

        :return: A Deferred that fires with a tuple of the queue to consume
                 messages from and a consumer tag.
        :rtype: Deferred of (pika.ClosableDeferredQueue, unicode str)
        """
        # TODO Handle errors appropriately
        if not self.connection:
            self.connection = yield self._deferred_connection
        if not self.channel:
            self.channel = yield self.connection.channel()

        # TODO Consider using ``passive=True`` on ``exchange_declare`` and
        # ``queue_declare``. This causes an error if the queue or exchange don't
        # already exist, which we could then turn into a HTTP 404. Allowing
        # requests to cause exchanges or queues to be created seems like an easy
        # DoS attack.
        yield self.channel.exchange_declare(exchange=exchange)
        yield self.channel.queue_declare(
            queue=queue,
            durable=True,
            auto_delete=False,
            arguments={'x-message-ttl': self.expire_ms}
        )
        # TODO investigate why this routing_key is used
        yield self.channel.queue_bind(
            exchange=exchange,
            queue=queue,
            routing_key=exchange + '-' + queue,
        )
        # TODO Maybe prefetch_count/size should be configurable
        yield self.channel.basic_qos(prefetch_count=5)
        deferred_queue, consumer_tag = yield self.channel.basic_consume(
            queue=queue,
            no_ack=False,
            exclusive=False,
            consumer_tag=None,
        )
        queue = RabbitQueue(queue=deferred_queue, consumer_tag=consumer_tag)
        defer.returnValue(queue)

    def render_GET(self, request):
        """
        Handle GET requests to this endpoint. Requests should be to
        ``/<exchange>/<queue.name>/``.
        """
        # If the request ended in a trailing / the final path section is ''.
        # This allows the trailing / on /<exchange>/<queue>/ to be optional.
        if request.postpath[-1] == '':
            request.postpath.pop()
        if len(request.postpath) != 2:
            response = JsonNotFound()
            return response.render(request)

        # TODO add checks here for a set of whitelisted exchanges and queues
        # or anyone can connect and drain, for example, the worker queue.

        # TODO set access control origin
        request.setHeader(u'Content-Type', u'text/event-stream; charset=utf-8')
        request.setHeader(u'Access-Control-Allow-Origin', u'*')

        # The queue the request subscribes to may be empty, and it may not have
        # anything in it for a long time. Calling ``request.write`` here
        # ensures the response headers are written to the client immediately.
        # TODO can't do this here, we need to check if Rabbit is alive and the
        # queue exists. If it doesn't we should 503/404 etc.
        request.write(b'')

        request_key = RequestKey(exchange=request.postpath[0], queue=request.postpath[1])
        request.notifyFinish().addBoth(self.request_closed, request, request_key)

        if request_key not in self.subscribers:
            # This is the first request for a particular queue
            subscription = {'queue': None, 'requests': [request]}
            self.subscribers[request_key] = subscription
            self.new_subscription(request_key)
        else:
            self.subscribers[request_key]['requests'].append(request)
        return server.NOT_DONE_YET

    def new_subscription(self, request_key):
        """
        Subscribe to a RabbitMQ queue.

        An entry will be made in the ``self.subscribers`` dictionary using the
        ``request_key`` provided as the dictionary key.

        :param request_key: A namedtuple containing the exchange and queue.
        :type  request_key: RequestKey
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
            subscription = self.subscribers[request_key]
            subscription['queue'] = rabbit_queue

            while True:
                channel, method, properties, body = yield rabbit_queue.queue.get()
                for request in subscription['requests']:
                    msg = u'data: ' + body.decode('utf-8') + u'\r\n\r\n'
                    request.write(msg.encode('utf-8'))
                yield channel.basic_ack(delivery_tag=method.delivery_tag)

        deferred_queue = self.queue(request_key.exchange, request_key.queue)
        deferred_queue.addCallback(write_requests)
        deferred_queue.addErrback(self.queue_error_handler, request_key)
        return deferred_queue

    def queue_error_handler(self, err, request_key):
        """
        Handle possible errors that occur in ``self.queue``
        """
        _log.info(str(err))
        if isinstance(err.value, error.ConnectionRefusedError):
            # RabbitMQ is down or refusing connections for some other reason;
            # Perform cleanup.
            for request in self.subscribers[request_key]['requests']:
                # TODO finish with 503
                request.finish()
        elif isinstance(err.value, pika_exceptions.ChannelClosed):
            # Return the reason the channel was closed, try to restart the channel
            for request in self.subscribers[request_key]['requests']:
                request.finish()
        else:
            _log.warning('Unhandled error: ' + str(err))

    def request_closed(self, err, request, request_key):
        """
        Remove a request from the map of queues to open requests.

        This is intended to be called when a request is finished or closed.
        It can be added to a request by using ``request.notifyFinish``.

        :param err:       unused
        :param request_key: The queue the request is attached to in
                          self.subscribers
        :param request: The request to remove from self.subscribers
        """
        _log.debug('Removing ' + str(request) + ' from ' + str(request_key))
        try:
            subscriber = self.subscribers[request_key]
            subscriber['requests'].remove(request)
            if not self.subscribers[request_key]['requests']:
                # The last request for this queue is finished so clean
                # up everything else.
                if subscriber['queue']:
                    subscriber['queue'].queue.close()
                self.subscribers.pop(request_key)
        except (ValueError, KeyError):
            pass


class JsonNotFound(resource.ErrorPage):
    """
    An HTTP 404 resource that optionally returns a JSON body with error details.
    """

    def __init__(self, status=404, brief=u'Not Found', detail=None):
        """
        Initialize the resource.

        If `detail` is a dictionary it will be JSON-serialized and returned
        as the response body.
        """
        # The parent class saves these values as self.code, self.brief,
        # and self.detail.
        resource.ErrorPage.__init__(self, status, brief, detail)

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
                u'detail': self.detail or u'Resource not found',
            }

        if isinstance(body, six.text_type):
            body = body.encode('utf-8')
        return body


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    site = server.Site(SSEServer())
    port = int(app_config.get('fmn.sse.webserver.tcp_port', 8080))
    reactor.listenTCP(port, site)
    reactor.run()
