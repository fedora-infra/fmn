import json
import logging
import uuid
import datetime
import pika
import pytz
import six
from fmn.consumer.backends.base import BaseBackend, shorten
import fedmsg.meta


def _format_message(msg, recipient, config):
    """
    Here we have to distinguish between two different kinds of messages that
    might arrive: the `raw` message from fedmsg itself and the product of a
    call to `fedmsg.meta.conglomerate(..)`

    example output from sse.py is below

      {
        "dom_id": "d38b2b6c-a3c9-4772-b6aa-0a70a6bee517",
        "date_time": "2008-09-03T20:56:35.450686Z",
        "icon": "https://apps.fedoraproject.org/packages/images/icons/package_128x128.png",
        "link": "https://pagure.io/<repo>/issue/148703615",
        "markup": "<a href="pagure.io/atelic">@atelic</a> opened a new ticket #148703615: \"Things are broken wat do\"",
        "secondary_icon": null,
      }
    """

    dom_id = six.text_type(uuid.uuid4())
    date_time = ''
    icon = ''
    link = ''
    markup = ''
    secondary_icon = ''
    username = ''
    subtitle = ''
    if not 'subtitle' in msg:
        # This handles normal, 'raw' messages which get passed through msg2*.
        # Tack a human-readable delta on the end so users know that fmn is
        # backlogged (if it is).
        if msg['timestamp']:
            date_time = msg['timestamp']
            date_time = datetime.datetime.fromtimestamp(date_time)
            date_time = date_time.replace(tzinfo=pytz.utc).isoformat()
        else:
            date_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).isoformat()

        icon = fedmsg.meta.msg2icon(msg, **config)
        link = fedmsg.meta.msg2link(msg, **config)
        secondary_icon = fedmsg.meta.msg2secondary_icon(msg, **config)
        username = fedmsg.meta.msg2agent(msg, **config)
        title = fedmsg.meta.msg2title(msg, **config)
        subtitle = fedmsg.meta.msg2subtitle(msg, **config)

    else:
        # This handles messages that have already been 'conglomerated'.
        title = u""
        subtitle = msg['subtitle']
        link = msg['link']

    if recipient['shorten_links']:
        link = shorten(link)
    event_link = ''
    if title and link:
        event_link = '<a href="' + link + '">' + title + '</a>'
    user_link = ''
    if username:
        user_link = '<a href="/'+username.encode('utf-8').replace("@", "")+'">'+username.encode('utf-8')+'</a>'

    markup = ''
    if user_link:
        markup += user_link.encode('utf-8')
    if event_link:
        markup += ' ' + event_link.encode('utf-8')
    if subtitle:
        markup += ' ' + subtitle.encode('utf-8')

    output = {"dom_id": str(dom_id),
              "date_time": str(date_time),
              "icon": str(icon),
              "link": str(link),
              "markup": str(markup),
              "secondary_icon": str(secondary_icon)
              }

    return json.dumps(output)


class SSEBackend(BaseBackend):
    __context_name__ = "sse"

    def __init__(self, *args, **kwargs):
        super(SSEBackend, self).__init__(*args, **kwargs)

    def send_msg(self, msg="hello world", username="user.id.fedoraproject.org"):
        username = username.encode('utf-8')
        self.log.debug("SSE: \t Sending msg to pika to queue " + username)
        CONFIG = fedmsg.config.load_config()
        host = CONFIG.get('fmn.pika.host', 'localhost')
        exchange = 'user'
        queue_name = username
        expire_ms = int(CONFIG.get('fmn.pika.msg_expiration', 3600))
        port = int(CONFIG.get('fmn.pika.port', 5672))

        fq = FeedQueue(host=host, exchange=exchange, expire_ms=expire_ms,
                       queue_name=queue_name, port=port, log=self.log)

        fq.push_message(msg)

    def handle(self, session, recipient, msg, streamline=False):
        self.log.debug("SSE: \t handle")
        short_message = _format_message(msg=msg, recipient=recipient, config=self.config)
        user = recipient['user']
        self.send_msg(short_message, user)

    def handle_batch(self, session, recipient, queued_messages):
        self.log.debug("SSE: \t handle batch")
        messages = [m.message for m in queued_messages]
        # Squash some messages into one conglomerate message
        # https://github.com/fedora-infra/datagrepper/issues/132
        messages = fedmsg.meta.conglomerate(messages, **self.config)
        for message in messages:
            self.handle(session, recipient, message, streamline=True)

    def handle_confirmation(self, session, confirmation):
        pass

class FeedQueue:
    def __init__(self, host='localhost',
                 exchange='',
                 queue_name='skrzepto.id.fedoraproject.org',
                 expire_ms=1*60*60*1000,
                 port=5672,
                 log=None):

        self.host = host
        self.exchange = exchange
        self.queue_name = queue_name
        self.expire_ms = expire_ms
        self.port = port

        if log:
            self.log = log
        else:
            self.log = logging.getLogger("fmn")

        self.channel, self.connection = self._get_pika_channel_connection()

    def _check_connection(self):
        if self.connection.is_closed:
            self.channel, self.connection = self._get_pika_channel_connection()

    def push_message(self, msg):
        self._check_connection()

        if self.channel.basic_publish(exchange=self.exchange,
                                      routing_key=self.exchange + '-' + self.queue_name,
                                      body=msg,
                                      properties=pika.BasicProperties(
                                          delivery_mode=2)):
            self.log.debug('SSE: FEEDQUE: \t message sent')
        else:
            self.log.debug('SSE: FEEDQUE: ERROR: \t message failed to send')

    def _get_pika_channel_connection(self):
        """ Connect to pika server and return channel and connection"""
        parameters = pika.ConnectionParameters(host=self.host, port=self.port)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange)
        channel.queue_declare(queue=self.queue_name, durable=True,
                              arguments={'x-message-ttl': self.expire_ms, })
        channel.queue_bind(queue=self.queue_name,
                           exchange=self.exchange,
                           routing_key=self.exchange + '-' + self.queue_name)
        return channel, connection

