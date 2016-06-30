#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
This is a sample implementation of a Twisted push producer/consumer system. It
consists of a TCP server which asks the user how many random integers they
want, and it sends the result set back to the user, one result per line,
and finally closes the connection.
"""
import json
import threading
from sys import stdout
from zope.interface import implements
from twisted.python.log import startLogging
from twisted.internet import interfaces, reactor, defer, task
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from FeedQueue import FeedQueue



class PikaProducer(object):
    """
    Send back messages stored in the queue requested
    """

    implements(interfaces.IPushProducer)

    def __init__(self, proto, identifier):
        self._proto = proto
        self._paused = False
        self.identifier = identifier
        self._stop_producing = False
        self.lc = task.LoopingCall(self.sendMessage)
        self.fq = FeedQueue()

    def pauseProducing(self):
        """
        When we've produced data too fast, pauseProducing() will be called
        (reentrantly from within resumeProducing's sendLine() method, most
        likely), so set a flag that causes production to pause temporarily.
        """
        self._paused = True
        print 'Pausing connection from %s' % self._proto.transport.getPeer()
        self.lc.stop()

    def sendMessage(self):
        print self._proto.connection_lost
        if self._proto.connection_lost:
            self.stopProducing()
        if self._paused:
            self.lc.stop()
        data = self.fq.receive_one_message()
        if data:
            self._proto.sendLine(json.dumps(data))

    def resumeProducing(self):
        """
        Resume producing integers.
        """
        t = threading.Thread(target=self.lc.start, args=(5,))
        #self.lc.start(5)
        t.start()

    def stopProducing(self):
        """
        When a consumer has died, stop producing data for good.
        """
        self._stop_producing = True
        self._proto.transport.unregisterProducer()
        self._proto.transport.loseConnection()
        self.lc.stop()


class ServerFeed(LineReceiver):
    """
    Serve up random integers.
    """
    connection_lost = False
    def connectionMade(self):
        """
        Once the connection is made we ask the client how many random integers
        the producer should return.
        """
        print 'Connection made from %s' % self.transport.getPeer()
        self.sendLine('Which feed do you want to join? /group/<groupname> or /user/<username>')

    def lineReceived(self, line):
        """
        This checks how many random integers the client expects in return and
        tells the producer to start generating the data.
        """
        if line:
            data = str(line.strip()).split('/')
            self.sendLine(line)
        else:
            data = ['user', 'skrzepto']

        if data[0] == '':
            data.pop(0)

        if data[0] not in ['user', 'group']:
            print('invalid data')
            self.transport.loseConnection()

        if data[0] == 'user' and '.id.fedoraproject.org' not in data[1]:
            data[1] = data[1] + '.id.fedoraproject.org'

        print 'Client requested section %s with hub %s' % (data[0], data[1])
        producer = PikaProducer(self, data[1])
        self.transport.registerProducer(producer, True)
        producer.resumeProducing()

    def connectionLost(self, reason):
        print 'Connection lost from %s' % self.transport.getPeer()
        self.connection_lost = True


#help: http://stackoverflow.com/questions/28199703/having-trouble-with-a-simple-twisted-chat-server

startLogging(stdout)
factory = Factory()
factory.protocol = ServerFeed
reactor.listenTCP(1234, factory)
reactor.run()