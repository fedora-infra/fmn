import json
import urllib2

import pika
from twisted.web.resource import Resource
from twisted.web import server
from twisted.internet import reactor
from twisted.python.util import println
from twisted.internet import interfaces, reactor, defer, task


def get_recent_posts():
    delta = "delta=86400"  # one day worth of data
    rows_per_page = "rows_per_page=50"
    url = "https://apps.fedoraproject.org/datagrepper/raw" + "?" + delta + "&" + rows_per_page
    request = urllib2.Request(url)
    contents = urllib2.urlopen(request).read()
    json_response = json.loads(contents)
    return json_response['raw_messages']


def receive_one_message(host='localhost',
                        queue_name='skrzepto.id.fedoraproject.org',
                        expire_ms=60000):
    # modified but src is below
    # src: http://stackoverflow.com/questions/9876227/rabbitmq-consume-one-message-if-exists-and-quit
    channel, connection = _get_pika_channel(host=host,
                                            queue_name=queue_name,
                                            expire_ms=expire_ms)
    method_frame, header_frame, body = channel.basic_get(queue=queue_name)
    if not method_frame:
        connection.close()
        return ''

    if method_frame.NAME == 'Basic.GetEmpty':
        connection.close()
        return ''
    else:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connection.close()
        #print body
        return body


def _get_pika_channel(host='localhost',
                      queue_name='skrzpeto.id.fedoraproject.org',
                      expire_ms=60000):
    """ Connect to pika server and return channel and connection"""
    parameters = pika.ConnectionParameters(host=host)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True,
                          arguments={'x-message-ttl': expire_ms, })
    return channel, connection


from twisted.web import server, resource
from twisted.internet import reactor

class Simple(resource.Resource):
    isLeaf = True
    #TODO: Add routes to inividual pages
    # eg.  /group/<groupname>   /user/<username>
    def render_GET(self, request):
        request.responseHeaders.addRawHeader(b"content-type",
                                             b"application/json")
        self.write_messages(request)
        lc = task.LoopingCall(self.write_messages, request)
        lc.start(2)  # this seems to not react fast enough after the client has closed and keeps running
        # seperate thread???
        #reactor.callLater(10, request.finish)
        return server.NOT_DONE_YET

    def write_messages(self, request):
        data = receive_one_message(expire_ms=24 * 60 * 60 * 1000)
        request.write(data)

site = server.Site(Simple())
reactor.listenTCP(8080, site)
reactor.run()

