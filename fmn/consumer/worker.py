# FMN worker figuring out for a fedmsg message the list of recipient and
# contexts


import json
import logging
import time
import random

import fmn.lib
import fmn.rules.utils
import fedmsg
import fedmsg.meta
import fedmsg_meta_fedora_infrastructure

from fedmsg_meta_fedora_infrastructure import fasshim

import pika

import fmn.consumer.fmn_fasshim

log = logging.getLogger("fmn")
log.setLevel('DEBUG')
CONFIG = fedmsg.config.load_config()
fedmsg.meta.make_processors(**CONFIG)

DB_URI = CONFIG.get('fmn.sqlalchemy.uri', None)
session = fmn.lib.models.init(DB_URI)

from dogpile.cache import make_region
_cache = make_region(
    key_mangler=lambda key: "fmn.consumer:dogpile:" + key
).configure(**CONFIG['fmn.rules.cache'])

valid_paths = fmn.lib.load_rules(root="fmn.rules")

OPTS = pika.ConnectionParameters(
    heartbeat_interval=0,
    retry_delay=2,
)


def get_preferences():
    print 'get_preferences'
    session = fmn.lib.models.init(DB_URI)
    prefs = fmn.lib.load_preferences(
        session, CONFIG, valid_paths,
        cull_disabled=True,
        cull_backends=['desktop']
    )
    session.close()
    print 'prefs retrieved'
    return prefs


def update_preferences(openid, prefs):
    log.info("Loading and caching preferences for %r" % openid)
    old_preferences = [
        p for p in prefs if p['user']['openid'] == openid]
    new_preferences = fmn.lib.load_preferences(
        session, CONFIG, valid_paths,
        cull_disabled=True,
        openid=openid,
        cull_backends=['desktop']
    )
    prefs.extend(new_preferences)
    for old_preference in old_preferences:
        prefs.remove(old_preference)

    return prefs


CNT = 0
PREFS = get_preferences()

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

connection = pika.BlockingConnection(OPTS)

def inform_workers(raw_msg, context, recipients):
    queue = 'backends'
    chan = connection.channel()
    chan.exchange_declare(exchange=queue)
    chan.queue_declare(queue, durable=True)

    print 'backends', context, recipients
    chan.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps({
            'context': context,
            'recipients': recipients,
            'raw_msg': raw_msg,
        }),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )
    chan.close()


def callback(ch, method, properties, body):
    start = time.time()

    global CNT, connection, PREFS
    CNT += 1
    raw_msg = json.loads(body)
    topic, msg = raw_msg['topic'], raw_msg['body']
    print topic

    # If the user has tweaked their preferences on the frontend, then
    # invalidate our entire in-memory cache of the fmn preferences
    # database.
    if '.fmn.' in topic:
        openid = msg['msg']['openid']
        PREFS = update_preferences(openid, PREFS)
        if topic == 'consumer.fmn.prefs.update':  # msg from the consumer
            log.debug(
                "Done with refreshing prefs.  %0.2fs %s",
                time.time() - start,msg['topic'])
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

    # Shuffle it so that not all threads step through the list in the same
    # order.  This should cut down on competition for the dogpile lock when
    # getting pkgdb info at startup.
    random.shuffle(PREFS)

    # And do the real work of comparing every rule against the message.
    t = time.time()
    results = fmn.lib.recipients(PREFS, msg, valid_paths, CONFIG)
    log.debug("results retrieved in: %0.2fs", time.time() - t)

    log.debug("Recipients found %i dt %0.2fs %s %s",
              len(results), time.time() - start,
              msg['msg_id'], msg['topic'])

    # Let's look at the results of our matching operation and send stuff
    # where we need to.
    for context, recipients in results.items():
        if not recipients:
            continue

        for attempt in range(3):
            try:
                inform_workers(raw_msg, context, recipients)
                break
            except:
                if attempt == 2:
                    raise

    ch.basic_ack(delivery_tag=method.delivery_tag)

    log.debug("Done.  %0.2fs %s %s",
              time.time() - start, msg['msg_id'], msg['topic'])


queue = 'refresh'
channel = connection.channel()
channel.exchange_declare(exchange=queue, type='fanout')
refresh_q = channel.queue_declare(exclusive=True)
refresh_q_name = refresh_q.method.queue
channel.queue_bind(exchange=queue, queue=refresh_q_name)

queue = 'workers'
channel.exchange_declare(exchange=queue, type='direct')
workers_q = channel.queue_declare(queue, durable=True)
channel.queue_bind(exchange=queue, queue=queue)

print 'started at %s workers' % workers_q.method.message_count
print 'started at %s refresh' % refresh_q.method.message_count

# Make sure we leave any other messages in the queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue)
channel.basic_consume(callback, queue=refresh_q_name)


try:
    print 'Starting consuming'
    channel.start_consuming()
except KeyboardInterrupt:
    channel.cancel()
    connection.close()
    session.close()
finally:
    print '%s tasks proceeded' % CNT
