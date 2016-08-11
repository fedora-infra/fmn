from twisted.internet import task
import fedmsg

from fmn.sse.FeedQueue import FeedQueue

Config = fedmsg.config.load_config()

import logging
logging.basicConfig(level=logging.DEBUG)
global_log = logging.getLogger("fedmsg")


class SSESubscriber:
    def __init__(self, log=None):
        self.connections = {}
        self.looping_calls = {}

        if log:
            self.logger = log
        else:
            self.logger = global_log

    def push_sse(self, msg, conn):
        try:
            msg = bytes.decode(msg)
        # This will raise in python2 where msg is a string, not bytes
        except TypeError:
            pass

        event_line = "data: {}\r\n\r\n".format(msg)
        try:
            event_line = event_line.encode('utf-8')
        except:
            pass

        conn.write(event_line)

    def write_messages_all_connections(self, key):
        '''
        :param key: example =['user', 'bob.id.fedoraproject.org']
        :return: None
        '''
        payload = self.get_payload(key=key)
        if payload:
            self.logger.info(payload)
            connections = self.get_connections(key=key)
            for req in connections:
                self.logger.info(req)
                self.push_sse(payload, req)

    def get_payload(self, key):
        '''
        :param key: example = ['user', 'bob.id.fedoraproject.org']
        :return: payload which is the message from the queue
        '''
        host = Config.get('fmn.sse.pika.host', 'localhost')
        exchange = key[0]  # Config.get('pika', 'exchange')
        queue_name = key[1]
        expire_ms = int(Config.get('fmn.sse.pika.msg_expiration', 3600000))
        port = int(Config.get('fmn.sse.pika.port', 5672))

        fq = FeedQueue(host=host, exchange=exchange, expire_ms=expire_ms,
                       queue_name=queue_name, port=port)
        data = fq.receive_one_message()
        if data:
            return str(data)
        else:
            return None

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
        self.logger.info('Succesfully added a connection ' + str(con))
        if not self.does_loopingcall_exist(key=key):
            self.add_looping_call(key)

    def remove_connection(self, con, key):
        '''
        :param con: eg. =['user', 'bob.id.fedoraproject.org']
        :param key:
        :return:
        '''
        self.logger.info("Removing connection")
        self.connections[key[0]][key[1]].remove(con)
        if not self.check_if_connections_exist_for_queue(key):
            self.stop_looping_call(key)

    def get_connections(self, key):
        return self.connections[key[0]][key[1]]

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
