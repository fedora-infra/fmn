# -*- coding: utf-8 -*-
"""
The FMN backend is a `Twisted`_ application that consumes messages that have
been queued by FMN workers and sends them to the user over the configured
medium (IRC, email, etc) by using "backends".

.. _Twisted: https://twistedmatrix.com/
"""
from __future__ import print_function


import json
import logging
import smtplib
import time

from fedmsg_meta_fedora_infrastructure import fasshim
from pika.adapters import twisted_connection
from twisted.internet import defer, reactor, protocol, task
import pika
import fedmsg
import fedmsg.meta
import fedmsg_meta_fedora_infrastructure

import fmn.lib
import fmn.rules.utils
import fmn.consumer.backends as fmn_backends
import fmn.consumer.producer as fmn_producers
import fmn.consumer.fmn_fasshim


logging.basicConfig(level=logging.DEBUG)
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

log.debug("Instantiating FMN backends")
backend_kwargs = dict(config=CONFIG)

# If debug is enabled, use the debug backend everywhere
if CONFIG.get('fmn.backends.debug', False):
    log.debug(' ** Use the DebugBackend as all backends **')
    backends = {
        'sse': fmn_backends.SSEBackend(**backend_kwargs),
        'email': fmn_backends.DebugBackend(**backend_kwargs),
        'irc': fmn_backends.IRCBackend(**backend_kwargs),
        'android': fmn_backends.DebugBackend(**backend_kwargs),
    }
else:
    backends = {
        'sse': fmn_backends.SSEBackend(**backend_kwargs),
        'email': fmn_backends.EmailBackend(**backend_kwargs),
        'irc': fmn_backends.IRCBackend(**backend_kwargs),
        'android': fmn_backends.GCMBackend(**backend_kwargs),
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

#: The entire set of user preferences from the database as a Python dictionary
#: in the format returned from :meth:`fmn.lib.models.Preference.__json__`.
PREFS = fmn.lib.load_preferences()


@defer.inlineCallbacks
def run(connection):
    """
    Ensure the various exchanges and queues are configured and set up a looping
    call in the reactor for :func:`.read` on the ``refresh`` and ``backends``
    queues.

    Args:
        connection (twisted_connection.TwistedProtocolConnection): The Pika
            RabbitMQ connection to use.
    """

    channel = yield connection.channel()
    yield channel.basic_qos(prefetch_count=1)

    queue = 'refresh'
    yield channel.exchange_declare(exchange=queue, type='fanout')
    result = yield channel.queue_declare(exclusive=False)
    queue_name = result.method.queue
    yield channel.queue_bind(exchange=queue, queue=queue_name)
    queue_object, consumer_tag = yield channel.basic_consume(queue=queue_name)
    lc = task.LoopingCall(read, queue_object)
    lc.start(0.01)

    queue = 'backends'
    yield channel.exchange_declare(exchange=queue, type='direct')
    yield channel.queue_declare(durable=True)
    yield channel.queue_bind(exchange=queue, queue=queue)
    queue_object2, consumer_tag2 = yield channel.basic_consume(queue=queue)
    lc2 = task.LoopingCall(read, queue_object2)
    lc2.start(0.01)


@defer.inlineCallbacks
def read(queue_object):
    """
    Read a single message from the queue and dispatch it to the proper backend.

    This is meant to be used with the looping call functionality of Twisted.

    Args:
        queue_object (twisted_connection.ClosableDeferredQueue): A queue of
            messages to consume.
    """
    ch, method, properties, body = yield queue_object.get()

    global CNT, PREFS
    CNT += 1

    start = time.time()

    data = json.loads(body)
    topic = data.get('topic', '')

    if '.fmn.' in topic:
        openid = data['body']['msg']['openid']
        fmn.lib.update_preferences(openid, PREFS)
        if topic == 'consumer.fmn.prefs.update':  # msg from the consumer
            print("Done with refreshing prefs.  %0.2fs %s" % (
                time.time() - start, data['topic']))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

    # This is a special handler for messages placed in the ``backends`` queue by
    # the :mod:`fmn.consumer.digests` module.

    # This module places messages in the queue in two different formats. The
    # first format is used when there is only one message in the digest, and
    # the second is used when there are multiple messages in the digest.

    # This is in dire need of refactoring, but for the moment this is used to
    # check to see if this is a special message by checking for the existence of
    # the ``function`` key which has a string value set to either ``handle`` or
    # ``handle_batch``, and then calling the appropriate backend function.
    function = data.get('function', '')
    if function:
        print("Got a function call to %s" % function)
        try:
            if function == 'handle':
                backend = backends[data['backend']]
                backend.handle(session,
                               data['recipient'],
                               data['msg'],
                               data['streamline'])
                ch.basic_ack(delivery_tag=method.delivery_tag)
            elif function == 'handle_batch':
                backend = backends[data['backend']]
                backend.handle_batch(session,
                                     data['recipient'],
                                     data['queued_messages'])
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                print("Unknown function")
            return
        except Exception:
            # Republishing the message will place the message at the back of
            # work queue so the message doesn't get lost, but also doesn't hold
            # up new messages.
            logging.exception('Message failed, requeueing')
            ch.basic_publish(exchange='', routing_key='backends', body=body,
                             properties=pika.BasicProperties(delivery_mode=2))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

    recipients, context, raw_msg = \
        data['recipients'], data['context'], data['raw_msg']['body']

    print("  Considering %r with %i recips" % (
        context, len(list(recipients))))

    backend = backends[context]
    for recipient in recipients:
        user = recipient['user']
        t = time.time()
        pref = PREFS.get('%s_%s' % (user, context))
        print("pref retrieved in: %0.2fs" % (time.time() - t))

        try:
            if pref.get('batch_delta') is None and pref.get('batch_count') is None:
                print("    Calling backend %r with %r" % (backend, recipient))
                t = time.time()
                backend.handle(session, recipient, raw_msg)
                print("Handled by backend in: %0.2fs" % (time.time() - t))
            else:
                print("    Queueing msg for digest")
                fmn.lib.models.QueuedMessage.enqueue(
                    session, user, context, raw_msg)
            if ('filter_oneshot' in recipient and recipient['filter_oneshot']):
                print("    Marking one-shot filter as fired")
                idx = recipient['filter_id']
                fltr = session.query(fmn.lib.models.Filter).get(idx)
                fltr.fired(session)
        except RuntimeError:
            yield ch.basic_nack(delivery_tag=method.delivery_tag)
            return
        except smtplib.SMTPSenderRefused:
            yield ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

    session.commit()

    yield ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Done.  %0.2fs %s %s" % (
              time.time() - start, raw_msg['msg_id'], raw_msg['topic']))


parameters = pika.ConnectionParameters()
cc = protocol.ClientCreator(
    reactor, twisted_connection.TwistedProtocolConnection, parameters)
host = CONFIG.get('fmn.pika.host', 'localhost')
port = int(CONFIG.get('fmn.pika.port', 5672))
d = cc.connectTCP(host=host, port=port)
d.addCallback(lambda protocol: protocol.ready)
d.addCallback(run)

# Here we schedule to producers to run periodically (with a default
# frequency of 10 seconds.
# Added value: Everything is nicely tied up with twisted in one app/place
# Cons: if one of the producer suddenly takes a real while to run, it will
# block the entire twisted reactor and thus all the backends with it.
# TODO: move to cron?
frequency = CONFIG.get('fmn.confirmation_frequency', 10)
confirmation_producer = fmn_producers.ConfirmationProducer(
    session, backends)
lc3 = task.LoopingCall(confirmation_producer.work)
lc3.start(frequency)


try:
    print('Starting consuming')
    reactor.run()
except KeyboardInterrupt:
    pass
finally:
    session.close()
    print('%s tasks proceeded' % CNT)
