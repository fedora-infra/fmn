"""
This is a `fedmsg consumer`_ that subscribes to every topic on the message bus
it is connected to. It has two tasks. The first is to place all incoming
messages into a RabbitMQ message queue. The second is to manage the FMN caches.

FMN makes heavy use of caches since it needs to know who owns what packages and
what user notification preferences are, both of which require expensive API
queries to `FAS`_, `pkgdb`_, or the database.

.. _fedmsg consumer: http://www.fedmsg.com/en/latest/consuming/#the-hub-consumer-approach
.. _FAS: https://admin.fedoraproject.org/accounts/
.. _pkgdb: https://admin.fedoraproject.org/pkgdb/
"""

import datetime
import logging
import time
import uuid

import fedmsg.consumers
import pika

import fmn.lib
import fmn.rules.utils
from fmn.consumer.util import (
    new_packager,
    new_badges_user,
    get_fas_email,
)


log = logging.getLogger("fmn")

OPTS = pika.ConnectionParameters(
    heartbeat_interval=0,
    retry_delay=2,
)


def notify_prefs_change(openid):
    """
    Publish a message to a fanout exchange notifying consumers about preference
    updates.

    Consumers can use these messages to refresh the process-local caches on a
    user-by-user basis. To recieve these messages, just bind the RabbitMQ
    queue you're using to the ``refresh`` fanout exchange.

    Messages are JSON-serialized and UTF-8 encoded.

    Example::

        {
            "topic": "consumer.fmn.prefs.update",
            "body": {
                "topic": "consumer.fmn.prefs.update",
                "msg_id": "<year>-<random-uuid>",
                "msg": {
                    "openid": "<user's openid who updated their preferences>"
                }
            }
        }
    """
    import json
    connection = pika.BlockingConnection(OPTS)
    msg_id = '%s-%s' % (datetime.datetime.utcnow().year, uuid.uuid4())
    queue = 'refresh'
    chan = connection.channel()
    chan.exchange_declare(exchange=queue, type='fanout')
    chan.basic_publish(
        exchange=queue,
        routing_key='',
        body=json.dumps({
            'topic': 'consumer.fmn.prefs.update',
            'body': {
                'topic': 'consumer.fmn.prefs.update',
                "msg_id": msg_id,
                'msg': {
                    "openid": openid,
                },

            },
        }),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )
    chan.close()
    connection.close()


class FMNConsumer(fedmsg.consumers.FedmsgConsumer):
    """
    A `fedmsg consumer`_ that subscribes to all topics and re-publishes all
    messages to the ``workers`` exchange.

    Attributes:
        topic (str): The topics this consumer is subscribed to. Set to ``*``
            (all topics).
        config_key (str): The key to set to ``True`` in the fedmsg config to
            enable this consumer. The key is ``fmn.consumer.enabled``.
    """
    topic = '*'
    config_key = 'fmn.consumer.enabled'

    def __init__(self, *args, **kwargs):
        log.debug("FMNConsumer initializing")
        super(FMNConsumer, self).__init__(*args, **kwargs)

        self.uri = self.hub.config.get('fmn.sqlalchemy.uri', None)
        self.autocreate = self.hub.config.get('fmn.autocreate', False)
        self.junk_suffixes = self.hub.config.get('fmn.junk_suffixes', [])
        self.ignored_copr_owners = self.hub.config.get('ignored_copr_owners',
                                                       [])

        if not self.uri:
            raise ValueError('fmn.sqlalchemy.uri must be present')

        log.debug("Loading rules from fmn.rules")
        self.valid_paths = fmn.lib.load_rules(root="fmn.rules")

        session = self.make_session()
        session.close()

        log.debug("FMNConsumer initialized")

    def make_session(self):
        """
        Initialize the database session and return it.

        Returns:
            sqlalchemy.orm.scoping.scoped_session: An SQLAlchemy scoped session.
                Calling it returns the current Session, creating it using the
                scoped_session.session_factory if not present.
        """
        return fmn.lib.models.init(self.uri)

    def consume(self, raw_msg):
        """
        This method is called when a message arrives on the fedmsg bus.

        Args:
            raw_msg (dict): The raw fedmsg deserialized to a Python dictionary.
        """
        session = self.make_session()
        try:
            self.work(session, raw_msg)
            session.commit()  # transaction is committed here
        except:
            session.rollback()  # rolls back the transaction
            raise

    def work(self, session, raw_msg):
        """
        This method is called when a message arrives on the fedmsg bus by the
        :meth:`.consume` method.

        Args:
            session (sqlalchemy.orm.session.Session): The SQLAlchemy session to use.
            raw_msg (dict): The raw fedmsg deserialized to a Python dictionary.
        """
        topic, msg = raw_msg['topic'], raw_msg['body']

        for suffix in self.junk_suffixes:
            if topic.endswith(suffix):
                log.debug("Dropping %r", topic)
                return

        # Ignore high-usage COPRs
        if topic.startswith('org.fedoraproject.prod.copr.') and \
                msg['msg'].get('owner') in self.ignored_copr_owners:
            log.debug('Dropping COPR %r by %r' % (topic, msg['msg']['owner']))
            return

        start = time.time()
        log.debug("FMNConsumer received %s %s", msg['msg_id'], msg['topic'])

        # First, do some cache management.  This can be confusing because there
        # are two different caches, with two different mechanisms, storing two
        # different kinds of data.  The first is a simple python dict that
        # contains the 'preferences' from the fmn database.  The second is a
        # dogpile.cache (potentially stored in memcached, but configurable from
        # /etc/fedmsg.d/).  The dogpile.cache cache stores pkgdb2
        # package-ownership relations.  Both caches are held for a very long
        # time and update themselves dynamically here.

        if '.fmn.' in topic:
            openid = msg['msg']['openid']
            notify_prefs_change(openid)

        # If a user has tweaked something in the pkgdb2 db, then invalidate our
        # dogpile cache.. but only the parts that have something to do with any
        # one of the users involved in the pkgdb2 interaction.  Note that a
        # 'username' here could be an actual username, or a group name like
        # 'group::infra-sig'.
        if '.pkgdb.' in topic:
            usernames = fedmsg.meta.msg2usernames(msg, **self.hub.config)
            for username in usernames:
                log.info("Invalidating pkgdb2 dogpile cache for %r" % username)
                target = fmn.rules.utils.get_packages_of_user
                fmn.rules.utils.invalidate_cache_for(
                    self.hub.config, target, username)

        # Create a local account with all the default rules if a user is
        # identified by one of our 'selectors'.  Here we can add all kinds of
        # new triggers that should create new FMN accounts.  At this point in
        # time we only create new accounts if 1) a new user is added to the
        # packager group or 2) someone logs into badges.fp.o for the first
        # time.
        if self.autocreate:
            selectors = [new_packager, new_badges_user]
            candidates = [fn(topic, msg) for fn in selectors]
            for username in candidates:
                if not username:
                    continue
                log.info("Autocreating account for %r" % username)
                openid = '%s.id.fedoraproject.org' % username
                openid_url = 'https://%s.id.fedoraproject.org' % username
                email = get_fas_email(self.hub.config, username)
                user = fmn.lib.models.User.get_or_create(
                    session, openid=openid, openid_url=openid_url,
                    create_defaults=True, detail_values=dict(email=email),
                )
                session.add(user)
                session.commit()
                notify_prefs_change(openid)

        # Do the same dogpile.cache invalidation trick that we did above, but
        # here do it for fas group membership changes.  (This is important
        # because someone could be in a group like the infra-sig which itself
        # has package-ownership relations in pkgdb.  If membership in that
        # group changes we need to sync fas relationships to catch up and route
        # messages to the new group members).
        if '.fas.group.' in topic:
            usernames = fedmsg.meta.msg2usernames(msg, **self.hub.config)
            for username in usernames:
                log.info("Invalidating fas cache for %r" % username)
                target = fmn.rules.utils.get_groups_of_user
                fmn.rules.utils.invalidate_cache_for(
                    self.hub.config, target, username)

        # With cache management done, we can move on to the real work.
        # Compute, based on our in-memory cache of preferences, who we think
        # should receive this message.

        import json
        connection = pika.BlockingConnection(OPTS)
        channel = connection.channel()
        channel.exchange_declare(exchange='workers')
        channel.queue_declare('workers', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='workers',
            body=json.dumps(raw_msg),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        channel.close()
        connection.close()

        log.debug("Done.  %0.2fs %s %s",
                  time.time() - start, msg['msg_id'], msg['topic'])

    def stop(self):
        """
        Gracefully halt this fedmsg consumer.
        """
        log.info("Cleaning up FMNConsumer.")
        super(FMNConsumer, self).stop()
