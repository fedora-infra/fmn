# FMN worker figuring out for a fedmsg message the list of recipient and
# contexts


import json
import logging
import time
import random

import pika
import fedmsg
import fedmsg.meta

import fmn.lib
import fmn.rules.utils
import backends as fmn_backends

from fedmsg_meta_fedora_infrastructure import fasshim

log = logging.getLogger("fmn")
CONFIG = fedmsg.config.load_config()
fedmsg.meta.make_processors(**CONFIG)
fasshim.make_fas_cache(**CONFIG)

CNT = 0

connection = pika.BlockingConnection()
channel = connection.channel()

ch = channel.queue_declare('backends', durable=True)
print 'started at', ch.method.message_count


log.debug("Instantiating FMN backends")
backend_kwargs = dict(config=CONFIG)
backends = {
    'email': fmn_backends.EmailBackend(**backend_kwargs),
    'irc': fmn_backends.IRCBackend(**backend_kwargs),
    'android': fmn_backends.GCMBackend(**backend_kwargs),
    #'rss': fmn_backends.RSSBackend,
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

# If debug is enabled, use the debug backend everywhere
if CONFIG.get('fmn.backends.debug', False):
    for key in backends:
        log.debug('Setting %s to use the DebugBackend' % key)
        backends[key] = fmn_backends.DebugBackend(**backend_kwargs)


def callback(ch, method, properties, body):
    start = time.time()

    global CNT
    CNT += 1

    start = time.time()

    data = json.loads(body)
    recipients, context, raw_msg = data['recipients'], data['context'], data['raw_msg']
    topic, msg = raw_msg['topic'], raw_msg['body']
    print topic, context
    log.debug("  Considering %r with %i recips" % (
        context, len(list(recipients))))

    session = fmn.lib.models.init(CONFIG.get('fmn.sqlalchemy.uri', None))
    backend = backends[context]
    for recipient in recipients:
        user = recipient['user']
        pref = fmn.lib.models.Preference.load(
            session, user, context)

        if not pref.should_batch:
            log.debug("    Calling backend %r with %r" % (
                backend, recipient))
            backend.handle(session, recipient, msg)
        else:
            log.debug("    Queueing msg for digest")
            fmn.lib.models.QueuedMessage.enqueue(
                session, user, context, msg)
        if ('filter_oneshot' in recipient
                and recipient['filter_oneshot']):
            log.debug("    Marking one-shot filter as fired")
            idx = recipient['filter_id']
            fltr = session.query(fmn.lib.models.Filter).get(idx)
            fltr.fired(session)
    session.commit()
    session.close()

    log.debug("Done.  %0.2fs %s %s",
              time.time() - start, msg['msg_id'], msg['topic'])

    channel.basic_ack(delivery_tag=method.delivery_tag)
    chan = channel.queue_declare('backends', durable=True)
    print chan.method.message_count

# Make sure we leave any other messages in the queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='backends')

try:
    print 'Starting consuming'
    channel.start_consuming()
except KeyboardInterrupt:
    channel.cancel()
    connection.close()
finally:
    print '%s tasks proceeded' % CNT
