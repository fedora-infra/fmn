import json
import logging

import fedmsg
import six
from twisted.internet import reactor
from twisted.web import server, resource

from fmn.sse.subscriber import SSESubscriber


log = logging.getLogger("fmn")
log.setLevel('DEBUG')
Config = fedmsg.config.load_config()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler(Config.get('fmn.sse.webserver.log', 'sse.log'))
# handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)


class SSEServer(resource.Resource):
    isLeaf = True
    subscribers = SSESubscriber(log=logger)

    def render_GET(self, request):
        if self.is_valid_path(request.postpath):
            request = self.add_headers(request)
            self.handle_request(request)
            request.notifyFinish().addBoth(self.responseFailed,
                                           request, request.postpath)
            return server.NOT_DONE_YET
        else:
            response = JsonNotFound()
            return response.render(request)

    def add_headers(self, request):
        request.setHeader('Content-Type', 'text/event-stream; charset=utf-8')
        request.setHeader("Access-Control-Allow-Origin", "*")
        return request

    def responseFailed(self, err, request, key):
        '''
        :param key: example input ["user", "bob.id.fedoraproject.org"]
        :param err:  why it failed
        :param request:  which connection disconnected or failed
        :return: remove the connection from the data structure
        '''
        self.subscribers.remove_connection(request, key=key)

    def is_valid_path(self, path):
        '''
        :param path: example ["user", "bob.id.fedoraproject.org"]
        :return: boolean
        '''
        if len(path) == 2 and path[0].decode('utf-8') in [u'group', u'user']:
            if path[0].decode('utf-8') == u'user':
                path[0] = u'user'
                if not path[1].decode('utf-8').endswith(u'.id.fedoraproject.org'):
                    path[1] = path[1].decode('utf-8') + u'.id.fedoraproject.org'
                return True
            elif path[0].decode('utf-8') == u'group':
                if path[1]:
                    return True
        return False

    def handle_request(self, request):
        # assumption is that we must of passed the if statement is a valid path
        # to get to this function
        p = request.postpath
        self.subscribers.add_connection(con=request, key=p)


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
    site = server.Site(SSEServer())
    reactor.listenTCP(int(Config.get('fmn.sse.webserver.tcp_port', 8080)), site)
    reactor.run()
