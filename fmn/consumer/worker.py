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

from fedmsg_meta_fedora_infrastructure import fasshim

import pika

log = logging.getLogger("fmn")
log.setLevel('DEBUG')
CONFIG = fedmsg.config.load_config()
fedmsg.meta.make_processors(**CONFIG)

DB_URI = CONFIG.get('fmn.sqlalchemy.uri', None)

from dogpile.cache import make_region
_cache = make_region(
    key_mangler=lambda key: "fmn.consumer:dogpile:" + key
).configure(**CONFIG['fmn.rules.cache'])

valid_paths = fmn.lib.load_rules(root="fmn.rules")


def get_preferences():
    print 'get_preferences'
    session = fmn.lib.models.init(DB_URI)
    prefs = fmn.lib.load_preferences(
        session, CONFIG, valid_paths,
        cull_disabled=True,
        cull_backends=['desktop']
    )
    session.close()
    _cache.set('preferences', get_preferences())


fasshim.make_fas_cache(**CONFIG)
get_preferences()

CNT = 0
connection = pika.BlockingConnection()
channel = connection.channel()

ch = channel.queue_declare('workers', durable=True)
print 'started at', ch.method.message_count


def callback(ch, method, properties, body):
    start = time.time()

    global CNT
    CNT += 1
    raw_msg = json.loads(body)

    #print body
    topic, msg = raw_msg['topic'], raw_msg['body']
    print topic

    # First, make a thread-local copy of our shared cached prefs
    session = fmn.lib.models.init(DB_URI)
    preferences = _cache.get_or_create('preferences', get_preferences)
    session.close()
    # Shuffle it so that not all threads step through the list in the same
    # order.  This should cut down on competition for the dogpile lock when
    # getting pkgdb info at startup.
    random.shuffle(preferences)
    # And do the real work of comparing every rule against the message.
    results = fmn.lib.recipients(preferences, msg, valid_paths, CONFIG)

    log.debug("Recipients found %i dt %0.2fs %s %s",
              len(results), time.time() - start,
              msg['msg_id'], msg['topic'])

    # Let's look at the results of our matching operation and send stuff
    # where we need to.

    for context, recipients in results.items():
        if not recipients:
            continue

        print context, recipients
        backend_chan = connection.channel()
        backend_chan.queue_declare('backends', durable=True)
        backend_chan.basic_publish(
            exchange='',
            routing_key='backends',
            body=json.dumps({
                'context': context,
                'recipients': recipients,
                'raw_msg': raw_msg,
            }),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        backend_chan.close()

    log.debug("Done.  %0.2fs %s %s",
              time.time() - start, msg['msg_id'], msg['topic'])

    channel.basic_ack(delivery_tag=method.delivery_tag)
    chan = channel.queue_declare('workers', durable=True)
    print chan.method.message_count

# Make sure we leave any other messages in the queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='workers')

try:
    print 'Starting consuming'
    channel.start_consuming()
except KeyboardInterrupt:
    channel.cancel()
    connection.close()
finally:
    print '%s tasks proceeded' % CNT
