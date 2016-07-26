import json
import logging

import fedmsg
from twisted.internet import reactor, task
from twisted.web import server, resource

from fmn.sse.FeedQueue import FeedQueue

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
    connections = {}
    isLeaf = True
    looping_calls = {}

    def render_GET(self, request):

        request = self.add_headers(request)
        request.write("")
        if self.is_valid_path(request.postpath):
            self.handle_request(request)
            request.notifyFinish().addBoth(self.responseFailed,
                                           request, request.postpath)
            # reactor.callLater(10, request.finish)
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
        self.remove_connection(request, key=key)

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
            self.add_connection(con=request, key=p)

    def invalid_request(self, request, code=404, reason="Invalid Request"):
        request.setResponseCode(code, reason)
        return json.dumps({"error": str(code) + ": " + reason})

    def get_payload(self, key):
        '''
        :param key: example = ['user', 'bob.id.fedoraproject.org']
        :return: payload which is the message from the queue
        '''
        host = Config.get('fmn.sse.pika.host', 'localhost')
        exchange = key[0]  # Config.get('pika', 'exchange')
        queue_name = key[1]
        expire_ms = int(Config.get('fmn.sse.pika.msg_expiration', 3600))
        port = int(Config.get('fmn.sse.pika.port', None))

        fq = FeedQueue(host=host, exchange=exchange, expire_ms=expire_ms,
                       queue_name=queue_name, port=port)
        data = fq.receive_one_message()
        if data:
            return str(data)
        else:
            return None

    def push_sse(self, msg, conn):
        event_line = "data: {}\r\n".format(msg)
        conn.write(event_line + '\r\n')

    def write_messages_all_connections(self, key):
        '''
        :param key: example =['user', 'bob.id.fedoraproject.org']
        :return: None
        '''
        payload = self.get_payload(key=key)
        if payload:
            logger.info(payload)
            for req in self.connections[key[0]][key[1]]:
                logger.info(req)
                self.push_sse(payload, req)

    def add_connection(self, con, key):
        '''
        :param con:
        :param key: example =['user', 'bob.id.fedoraproject.org']
        :return: None
        '''
        if key[0] in self.connections:
            if key[1] in self.connections[key[0]]:
                self.connections[key[0]][key[1]].append(con)
            else:
                self.connections[key[0]][key[1]] = [con]
        else:
            self.connections[key[0]] = {}
            self.connections[key[0]][key[1]] = [con]
        logger.info('Succesfully added a connection ' + str(con))
        if not self.does_loopingcall_exist(key=key):
            self.add_looping_call(key)

    def check_if_connections_exist_for_queue(self, key):
        '''
        :param key: example =['user', 'bob.id.fedoraproject.org']
        :return: boolean
        '''
        # not liking this too much, this may throw a key error but i know that
        # connections were added before this called has been made and the worst
        # case it should be []
        if self.connections[key[0]][key[1]]:
            return True
        else:
            return False

    def does_loopingcall_exist(self, key):
        '''
        :param key: example =['user', 'bob.id.fedoraproject.org'])
        :return:
        '''
        if key[0] in self.looping_calls \
                and key[1] in self.looping_calls[key[0]]:
            return True
        else:
            return False

    def add_looping_call(self, key):
        '''
        :param key: eg. =['user', 'bob.id.fedoraproject.org']
        :return:
        '''
        if not key[0] in self.looping_calls:
            self.looping_calls[key[0]] = {}

        self.looping_calls[key[0]][key[1]] = task.LoopingCall(
            self.write_messages_all_connections, key)
        self.start_looping_call(key=key)

    def start_looping_call(self, key):
        '''
        :param key: eg. =['user', 'bob.id.fedoraproject.org']
        :return:
        '''
        if not self.looping_calls[key[0]][key[1]].running:
            self.looping_calls[key[0]][key[1]].start(1)

    def stop_looping_call(self, key):
        '''
        :param key: eg. =['user', 'bob.id.fedoraproject.org']
        :return:
        '''
        if self.looping_calls[key[0]][key[1]].running:
            self.looping_calls[key[0]][key[1]].stop()
        del self.looping_calls[key[0]][key[1]]

    def remove_connection(self, con, key):
        '''
        :param con: eg. =['user', 'bob.id.fedoraproject.org']
        :param key:
        :return:
        '''
        logger.info("Removing connection")
        self.connections[key[0]][key[1]].remove(con)
        if not self.check_if_connections_exist_for_queue(key):
            self.stop_looping_call(key)


if __name__ == "__main__":
    site = server.Site(SSEServer())
    reactor.listenTCP(int(Config.get('fmn.sse.webserver.tcp_port', 8080)), site)
    reactor.run()
