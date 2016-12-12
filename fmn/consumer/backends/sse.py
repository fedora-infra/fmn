from __future__ import absolute_import, unicode_literals

from gettext import gettext as _
import json
import logging
import uuid
import datetime

import pika
import pytz
import six
import fedmsg.meta
from pika.adapters import twisted_connection
from twisted.internet import reactor, protocol, defer

from fmn.consumer.backends.base import BaseBackend, shorten


_log = logging.getLogger(__name__)


class SSEBackend(BaseBackend):
    """
    This backend is responsible for the creation of RabbitMQ exchanges and
    queues and the re-publication of messages for consumption by the Server-
    Sent Events server.

    Messages are pulled off the "backend" queue and passed to this class, which
    formats them appropriately and pushes them back onto the appropriate
    exchange.
    """
    __context_name__ = "sse"

    def __init__(self, config):
        super(SSEBackend, self).__init__(config)

        self.expire_ms = int(self.config.get('fmn.pika.msg_expiration', 3600000))
        self.amqp_host = self.config.get('fmn.pika.host', 'localhost')
        self.amqp_port = int(self.config.get('fmn.pika.port', 5672))
        self.amqp_parameters = pika.ConnectionParameters(self.amqp_host, self.amqp_port)
        cc = protocol.ClientCreator(
            reactor,
            twisted_connection.TwistedProtocolConnection,
            self.amqp_parameters,
        )
        self._deferred_connection = cc.connectTCP(self.amqp_host, self.amqp_port)
        self._deferred_connection.addCallback(lambda conn: conn.ready)
        self.connection = None
        self.channel = None

    @defer.inlineCallbacks
    def handle(self, session, recipient, msg, streamline=False):
        """
        Handle sending a single message to one recipient.

        :param session:     The SQLAlchemy database session to use.
        :type  session:     sqlalchemy.orm.session.Session
        :param recipient:   The recipient of the message and their settings.
                            This controls what RabbitMQ queue the message ends
                            up in.
        :type recipient:    dict
        :param msg:         The message to send to the user.
        :type  msg:         dict
        :param streamline:  unused
        :param streamline:  boolean
        """
        short_message = self._format_message(msg, recipient)
        user = recipient['user']
        # TODO figure out when it's a group message
        queue = 'user-' + user
        _log.debug(_('Handling a message for {user} via server-sent '
                     'events').format(user=user))

        if not self.connection:
            self.connection = yield self._deferred_connection
        if not self.channel:
            self.channel = yield self.connection.channel()
        yield self.channel.queue_declare(
                queue=queue, durable=True, auto_delete=False,
                arguments={'x-message-ttl': self.expire_ms})

        # TODO consider confirming message delivery and retrying
        # on failure
        yield self.channel.basic_publish(
            exchange='',  # Publish to the default exchange
            routing_key=queue,
            body=short_message,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def handle_batch(self, session, recipient, queued_messages):
        """
        Handle sending a set of one or more messages to one recipient.

        :param session:     The SQLAlchemy database session to use.
        :type  session:     sqlalchemy.orm.session.Session
        :param recipient:   The recipient of the messages and their settings.
                            This controls what RabbitMQ queue the message ends
                            up in.
        :type recipient:    dict
        :param msg:         The messages to send to the user.
        :type  msg:         dict
        """
        message = _('Batching {count} messages for delivery via server-sent'
                    ' events').format(count=len(queued_messages))
        _log.debug(message)
        messages = [m.message for m in queued_messages]
        # Squash some messages into one conglomerate message
        # https://github.com/fedora-infra/datagrepper/issues/132
        messages = fedmsg.meta.conglomerate(messages, **self.config)
        for message in messages:
            self.handle(session, recipient, message)

    def handle_confirmation(self, session, confirmation):
        """
        This is an unimplemented method required by the parent class.
        """
        pass

    def _format_message(self, msg, recipient):
        """
        Here we have to distinguish between two different kinds of messages that
        might arrive: the `raw` message from fedmsg itself and the product of a
        call to `fedmsg.meta.conglomerate(..)` by way of ``handle_batch``.

        The format from `fedmsg.meta.conglomerate(..)` should be::

          {
            'subtitle': 'relrod pushed commits to ghc and 487 other packages',
            'link': None,  # This could be something.
            'icon': 'https://that-git-logo',
            'secondary_icon': 'https://that-relrod-avatar',
            'start_time': some_timestamp,
            'end_time': some_other_timestamp,
            'human_time': '5 minutes ago',
            'usernames': ['relrod'],
            'packages': ['ghc', 'nethack', ... ],
            'topics': ['org.fedoraproject.prod.git.receive'],
            'categories': ['git'],
            'msg_ids': {
                '2014-abcde': {
                    'subtitle': 'relrod pushed some commits to ghc',
                    'title': 'git.receive',
                    'link': 'http://...',
                    'icon': 'http://...',
                },
                '2014-bcdef': {
                    'subtitle': 'relrod pushed some commits to nethack',
                    'title': 'git.receive',
                    'link': 'http://...',
                    'icon': 'http://...',
                },
            },
          }

        We assume that if the ``msg_ids`` key is present, the message is a
        conglomerated message. If this key is not present, the message will
        be handed to ``fedmsg.meta.msg2*`` methods to extract the necessary
        information.

        The formatted message is a dictionary in the following form:

        {
          "dom_id": "d38b2b6c-a3c9-4772-b6aa-0a70a6bee517",
          "date_time": "2008-09-03T20:56:35.450686Z",
          "icon": "https://apps.fedoraproject.org/packages/images/icons/package_128x128.png",
          "link": "https://pagure.io/<repo>/issue/148703615",
          "markup": "<a href="http://example.com/">Marked up message summary</a>",
          "secondary_icon": null,
        }

        :param msg:         The messages to send to the user.
        :type  msg:         dict
        :param recipient:   The recipient of the messages and their settings.
                            This controls what RabbitMQ queue the message ends
                            up in.
        :type recipient:    dict

        :return: A UTF-8-encoded JSON-serialized message.
        :rtype:  bytes
        """
        conglomerated = 'msg_ids' in msg
        dom_id = six.text_type(uuid.uuid4())
        date_time = ''
        icon = ''
        link = ''
        markup = ''
        secondary_icon = ''
        username = ''
        subtitle = ''

        if conglomerated:
            # This handles messages that have already been 'conglomerated'.
            title = ''
            subtitle = msg['subtitle']
            link = msg['link']
        else:
            # This handles normal, 'raw' messages which get passed through msg2*.
            # Tack a human-readable delta on the end so users know that fmn is
            # backlogged (if it is).
            if msg['timestamp']:
                date_time = msg['timestamp']
                date_time = datetime.datetime.fromtimestamp(date_time)
                date_time = date_time.replace(tzinfo=pytz.utc).isoformat()
            else:
                date_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).isoformat()

            icon = fedmsg.meta.msg2icon(msg, **self.config)
            link = fedmsg.meta.msg2link(msg, **self.config)
            secondary_icon = fedmsg.meta.msg2secondary_icon(msg, **self.config)
            username = fedmsg.meta.msg2agent(msg, **self.config)
            title = fedmsg.meta.msg2title(msg, **self.config)
            subtitle = fedmsg.meta.msg2subtitle(msg, **self.config)

        if recipient['shorten_links']:
            link = shorten(link)
        event_link = ''
        if title and link:
            event_link = '<a href="' + link + '">' + title + '</a>'
        user_link = ''
        if username:
            user_link = '<a href="/' + username.replace("@", "") + '">' + username + '</a>'

        markup = ''
        if user_link:
            markup += user_link
        if event_link:
            markup += ' ' + event_link
        if subtitle:
            markup += ' ' + subtitle
        markup = markup.strip()

        output = {
            'dom_id': dom_id,
            'date_time': date_time,
            'icon': icon,
            'link': link,
            'markup': markup,
            'secondary_icon': secondary_icon
        }

        return json.dumps(output)
