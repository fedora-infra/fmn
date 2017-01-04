# FMN worker calculating and sending digests
from __future__ import print_function


import json
import logging

import pika
import fedmsg
import fedmsg.meta
import fedmsg_meta_fedora_infrastructure

from twisted.internet import reactor, task

import fmn.lib
import fmn.rules.utils
import fmn.consumer.producer as fmn_producers

import fmn.consumer.fmn_fasshim
from fedmsg_meta_fedora_infrastructure import fasshim

log = logging.getLogger("fmn")
log.setLevel('DEBUG')
CONFIG = fedmsg.config.load_config()
fedmsg.meta.make_processors(**CONFIG)

DB_URI = CONFIG.get('fmn.sqlalchemy.uri', None)
session = fmn.lib.models.init(DB_URI)

fmn.consumer.fmn_fasshim.make_fas_cache(**CONFIG)
# Monkey patch fedmsg_meta modules
fasshim.nick2fas = fmn.consumer.fmn_fasshim.nick2fas
fasshim.email2fas = fmn.consumer.fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.supybot.nick2fas = \
    fmn.consumer.fmn_fasshim.nick2fas
fedmsg_meta_fedora_infrastructure.anitya.email2fas = \
    fmn.consumer.fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.bz.email2fas = \
    fmn.consumer.fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.mailman3.email2fas = \
    fmn.consumer.fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.pagure.email2fas = \
    fmn.consumer.fmn_fasshim.email2fas

CNT = 0

log.debug("Instantiating FMN digest producer")
backend_kwargs = dict(config=CONFIG)


OPTS = pika.ConnectionParameters(
    heartbeat_interval=0,
    retry_delay=2,
)
connection = pika.BlockingConnection(OPTS)


class FakeBackend(object):
    def inform_workers(self, body):
        queue = 'backends'
        chan = self.connection.channel()
        chan.exchange_declare(exchange=queue)
        chan.queue_declare(queue, durable=True)

        body['backend'] = self.name

        chan.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        chan.close()

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection

    def handle(self, session, recipient, msg, streamline=False):
        self.inform_workers({
            'function': 'handle',
            'recipient': recipient,
            'msg': msg,
            'streamline': streamline})

    def handle_batch(self, session, recipient, queued_messages):
        self.inform_workers({
            'function': 'handle_batch',
            'recipient': recipient,
            'queued_messages': queued_messages})


backends = {
    'email': FakeBackend('email', connection),
    'irc': FakeBackend('irc', connection),
    'android': FakeBackend('android', connection),
}

# But, disable any of those backends that don't appear explicitly in
# our config.
for key, value in backends.items():
    if key not in CONFIG['fmn.backends']:
        del backends[key]

# Also, check that we don't have something enabled that's not explicit
for key in CONFIG['fmn.backends']:
    if key not in backends:
        raise ValueError("%r in fmn.backends (%r) is invalid" % (
            key, CONFIG['fmn.backends']))


frequency = CONFIG.get('fmn.digest_frequency', 10)
digest_producer = fmn_producers.DigestProducer(
    session, backends)
lc4 = task.LoopingCall(digest_producer.work)
lc4.start(frequency)


try:
    print('Starting producing')
    reactor.run()
finally:
    connection.close()
    session.close()
