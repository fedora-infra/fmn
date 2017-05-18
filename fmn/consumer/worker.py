"""
This is a runnable Python module that uses Twisted to consume AMQP messages
processed by the :class:`fmn.consumer.consumer.FMNConsumer` `fedmsg consumer`_.

It determines a list of recipients and contexts for each fedmsg and constructs
a new message using the initial fedmsg and the recipient and context list.

It then publishes these messages to the ``backends`` exchange which is consumed
by the :mod:`fmn.consumer.backend` module's Twisted application.

.. _fedmsg consumer:
    http://www.fedmsg.com/en/latest/consuming/#the-hub-consumer-approach
"""
from __future__ import print_function

import json
import logging
import time

from dogpile.cache import make_region
from fedmsg_meta_fedora_infrastructure import fasshim
import fedmsg
import fedmsg.meta
import fedmsg_meta_fedora_infrastructure
import pika

import fmn.lib
import fmn.rules.utils
import fmn.consumer.fmn_fasshim


log = logging.getLogger("fmn")
log.setLevel('DEBUG')
CONFIG = fedmsg.config.load_config()
fedmsg.meta.make_processors(**CONFIG)

DB_URI = CONFIG.get('fmn.sqlalchemy.uri', None)
session = fmn.lib.models.init(DB_URI)

_cache = make_region(
    key_mangler=lambda key: "fmn.consumer:dogpile:" + key
).configure(**CONFIG['fmn.rules.cache'].copy())

valid_paths = fmn.lib.load_rules(root="fmn.rules")

OPTS = pika.ConnectionParameters(
    heartbeat_interval=0,
    retry_delay=2,
)


CNT = 0

#: The entire set of user preferences from the database as a Python dictionary
#: in the format returned from :meth:`fmn.lib.models.Preference.__json__`.
PREFS = fmn.lib.load_preferences(cull_disabled=True, cull_backends=['desktop'])

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
    """
    Publish a message to the backends exchange for the backend to send to
    users.

    Args:
        raw_msg (dict): The original fedmsg that triggered this event.
        context (str): The type of backend to use (e.g. 'irc' or 'sse')
        recipients (list): A list of recipients. The recipient is a dictionary
            in the format::

                {
                  "triggered_by_links": true,
                  "None": "sse-jcline.id.fedoraproject.org",
                  "markup_messages": false,
                  "user": "jcline.id.fedoraproject.org",
                  "filter_name": "hose",
                  "filter_oneshot": false,
                  "filter_id": 7,
                  "shorten_links": false,
                  "verbose": true,
                }

            The values of these keys will vary based on user settings.
    """
    queue = 'backends'
    chan = connection.channel()
    chan.exchange_declare(exchange=queue)
    chan.queue_declare(queue, durable=True)

    print('backends', context, recipients)
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
    """
    The callback attached to the Pika consumer.

    This callback is called when a new message is pushed to the consumer by
    RabbitMQ. The message is from the :class:`fmn.consumer.consumer.FMNConsumer`
    and its format will either be the raw fedmsg or a notification to update the
    local caches. This message is dispatched by
    :func:`fmn.consumer.consumer.notify_prefs_change` and its format is documented
    on the function.
    """
    start = time.time()

    global CNT, connection, PREFS
    CNT += 1
    raw_msg = json.loads(body)
    topic, msg = raw_msg['topic'], raw_msg['body']
    print(topic)

    # If the user has tweaked their preferences on the frontend, then
    # invalidate our entire in-memory cache of the fmn preferences
    # database.
    if '.fmn.' in topic:
        openid = msg['msg']['openid']
        fmn.lib.update_preferences(openid, PREFS)
        if topic == 'consumer.fmn.prefs.update':  # msg from the consumer
            print("Done with refreshing prefs.  %0.2fs %s" % (
                time.time() - start, msg['topic']))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

    # And do the real work of comparing every rule against the message.
    t = time.time()
    results = fmn.lib.recipients(PREFS, msg, valid_paths, CONFIG)
    print("results retrieved in: %0.2fs" % (time.time() - t))

    print("Recipients found %i dt %0.2fs %s %s" % (
              len(results), time.time() - start,
              msg['msg_id'], msg['topic']))

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

    print("Done.  %0.2fs %s %s" % (
        time.time() - start, msg['msg_id'], msg['topic']))


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

print('started at %s workers' % workers_q.method.message_count)
print('started at %s refresh' % refresh_q.method.message_count)

# Make sure we leave any other messages in the queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue)
channel.basic_consume(callback, queue=refresh_q_name)


try:
    print('Starting consuming')
    channel.start_consuming()
except KeyboardInterrupt:
    channel.cancel()
    connection.close()
    session.close()
finally:
    print('%s tasks proceeded' % CNT)
