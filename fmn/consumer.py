"""
This is a `fedmsg consumer`_ that subscribes to every topic on the message bus
it is connected to. It has two tasks. The first is to place all incoming
messages into a RabbitMQ message queue. The second is to manage the FMN caches.

FMN makes heavy use of caches since it needs to know who owns what packages and
what user notification preferences are, both of which require expensive API
queries to `FAS`_, `pkgdb`_, or the database.

.. _fedmsg consumer: https://fedmsg.readthedocs.io/en/stable/subscribing/#consumer-approach
.. _FAS: https://admin.fedoraproject.org/accounts/
.. _pkgdb: https://admin.fedoraproject.org/pkgdb/
"""

import logging

import fedmsg.consumers
import kombu

import fmn.lib
import fmn.rules.utils
from fmn import config
from fmn.celery import RELOAD_CACHE_EXCHANGE_NAME
from .util import (
    new_packager,
    new_badges_user,
    get_fas_email,
    get_fasjson_email
)
from fmn.tasks import find_recipients, REFRESH_CACHE_TOPIC, heat_fas_cache


log = logging.getLogger("fmn")
_log = logging.getLogger(__name__)


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
    config_key = 'fmn.consumer.enabled'

    def __init__(self, hub, *args, **kwargs):
        self.topic = config.app_conf['fmn.topics']

        _log.info("FMNConsumer initializing")
        super(FMNConsumer, self).__init__(hub, *args, **kwargs)

        self.uri = config.app_conf['fmn.sqlalchemy.uri']
        self.autocreate = config.app_conf['fmn.autocreate']
        self.junk_suffixes = config.app_conf['fmn.junk_suffixes']
        self.ignored_copr_owners = config.app_conf['ignored_copr_owners']

        heat_fas_cache.apply_async()

        _log.info("Loading rules from fmn.rules")
        self.valid_paths = fmn.lib.load_rules(root="fmn.rules")

        session = self.make_session()
        session.close()

        _log.info("FMNConsumer initialized")

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

        _log.info("FMNConsumer received %s %s", msg['msg_id'], msg['topic'])

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
            _log.info('Broadcasting message to Celery workers to update cache for %s', openid)
            find_recipients.apply_async(
                ({'topic': 'fmn.internal.refresh_cache', 'body': openid},),
                exchange=RELOAD_CACHE_EXCHANGE_NAME,
                routing_key=config.app_conf['celery']['task_default_queue'],
            )

        # If a user has tweaked something in the pkgdb2 db, then invalidate our
        # dogpile cache.. but only the parts that have something to do with any
        # one of the users involved in the pkgdb2 interaction.  Note that a
        # 'username' here could be an actual username, or a group name like
        # 'group::infra-sig'.
        if '.pkgdb.' in topic:
            usernames = fedmsg.meta.msg2usernames(msg, **config.app_conf)
            for username in usernames:
                log.info("Invalidating pkgdb2 dogpile cache for %r" % username)
                target = fmn.rules.utils.get_packages_of_user
                fmn.rules.utils.invalidate_cache_for(
                    config.app_conf, target, username)

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
                fasjson = config.app_conf.get("fasjson", {}).get("active")
                if fasjson:
                    email = get_fasjson_email(config.app_conf, username)
                else:
                    email = get_fas_email(config.app_conf, username)
                user = fmn.lib.models.User.get_or_create(
                    session, openid=openid, openid_url=openid_url,
                    create_defaults=True, detail_values=dict(email=email),
                )
                session.add(user)
                session.commit()
                _log.info('Broadcasting message to Celery workers to update cache for %s', openid)
                find_recipients.apply_async(
                    ({'topic': REFRESH_CACHE_TOPIC, 'body': openid},),
                    exchange=RELOAD_CACHE_EXCHANGE_NAME,
                )

        # Do the same dogpile.cache invalidation trick that we did above, but
        # here do it for fas group membership changes.  (This is important
        # because someone could be in a group like the infra-sig which itself
        # has package-ownership relations in pkgdb.  If membership in that
        # group changes we need to sync fas relationships to catch up and route
        # messages to the new group members).
        if '.fas.group.' in topic:
            usernames = fedmsg.meta.msg2usernames(msg, **config.app_conf)
            for username in usernames:
                log.info("Invalidating fas cache for %r" % username)
                target = fmn.rules.utils.get_groups_of_user
                fmn.rules.utils.invalidate_cache_for(config.app_conf, target, username)

        # Finding recipients is computationally quite expensive so it's handled
        # by Celery worker processes. The results are then dropped into an AMQP
        # queue and processed by the backends.
        try:
            find_recipients.apply_async((raw_msg,))
        except kombu.exceptions.OperationalError:
            _log.exception('Dispatching task to find recipients failed')

    def stop(self):
        """
        Gracefully halt this fedmsg consumer.
        """
        log.info("Cleaning up FMNConsumer.")
        super(FMNConsumer, self).stop()
