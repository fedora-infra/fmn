import json
import logging

import fedmsg
from twisted.internet import reactor, task
from twisted.web import server, resource

from subscriber import SSESubscriber

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
        request.write("")
        if self.is_valid_path(request.postpath):
            self.handle_request(request)
            request.notifyFinish().addBoth(self.responseFailed,
                                           request, request.postpath)
            return server.NOT_DONE_YET
        else:
            return self.invalid_request(request=request,
                                        code=403,
                                        reason="Invalid Path")

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
        logger.error('Connection was disconnected from ' + str(request) +
                     'removing from active connections')
        self.subscribers.remove_connection(request, key=key)

    def is_valid_path(self, path):
        '''
        :param path: example ["user", "bob.id.fedoraproject.org"]
        :return: boolean
        '''
        if len(path) == 2 and path[0] in ['group', 'user']:
            if path[0] == 'user':
                if not path[1].endswith('.id.fedoraproject.org'):
                    path[1] += '.id.fedoraproject.org'
                return True
            elif path[0] == 'group':
                if path[1]:
                    return True
        return False

    def handle_request(self, request):
        p = request.postpath
        if self.is_valid_path(path=p):
            self.subscribers.add_connection(con=request, key=p)

    def invalid_request(self, request, code=404, reason="Invalid Request"):
        request.setResponseCode(code, reason)
        return json.dumps({"error": str(code) + ": " + reason})


if __name__ == "__main__":
    site = server.Site(SSEServer())
    reactor.listenTCP(int(Config.get('fmn.sse.webserver.tcp_port', 8080)), site)
    reactor.run()
