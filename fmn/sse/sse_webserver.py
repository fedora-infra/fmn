import json
import logging

import fedmsg
from fmn.sse.subscriber import SSESubscriber
from twisted.internet import reactor, task
from twisted.web import server, resource


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
        request = self.add_headers(request)
        request.write(b"")
        if self.is_valid_path(request.postpath):
            self.handle_request(request)
            request.notifyFinish().addBoth(self.responseFailed,
                                           request, request.postpath)
            return server.NOT_DONE_YET
        else:
            return self.invalid_request(request=request,
                                        code=403,
                                        reason='Invalid Path')

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

    def invalid_request(self, request, code=404, reason="Invalid Request"):
        request.setResponseCode(code, str.encode(reason))
        return json.dumps({"error": str(code) + ": " + reason})


if __name__ == "__main__":
    site = server.Site(SSEServer())
    reactor.listenTCP(int(Config.get('fmn.sse.webserver.tcp_port', 8080)), site)
    reactor.run()
