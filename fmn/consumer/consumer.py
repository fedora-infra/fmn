# An example fedmsg koji consumer

import threading
import time
import random

import fedmsg.consumers
import fmn.lib
import fmn.rules.utils
import backends as fmn_backends

from dogpile.cache import make_region
_cache = make_region(
    key_mangler=lambda key: "fmn.consumer:dogpile:" + key
)

from fmn.consumer.util import (
    new_packager,
    new_badges_user,
    get_fas_email,
    load_preferences,
)

import logging
log = logging.getLogger("fmn")


class FMNConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = '*'
    config_key = 'fmn.consumer.enabled'

    def __init__(self, *args, **kwargs):
        log.debug("FMNConsumer initializing")
        super(FMNConsumer, self).__init__(*args, **kwargs)

        self.uri = self.hub.config.get('fmn.sqlalchemy.uri', None)
        self.autocreate = self.hub.config.get('fmn.autocreate', False)
        self.junk_suffixes = self.hub.config.get('fmn.junk_suffixes', [])

        if not self.uri:
            raise ValueError('fmn.sqlalchemy.uri must be present')

        log.debug("Loading rules from fmn.rules")
        self.valid_paths = fmn.lib.load_rules(root="fmn.rules")

        # Initialize our dogpile cache of the FMN preferences database
        if not _cache.is_configured:
            _cache.configure(
                **self.hub.config['fmn.rules.cache']
            )

        session = self.make_session()
        self.set_cache(session)
        session.close()

        log.debug("FMNConsumer initialized")

    def set_cache(self, session, openid=None):
        log.info("Loading and caching all preferences for all users")
        return _cache.get_or_create(
            'preferences', load_preferences,
            (session, self.hub.config, self.valid_paths)
        )

    def make_session(self):
        return fmn.lib.models.init(self.uri)

    def consume(self, raw_msg):
        session = self.make_session()
        try:
            self.work(session, raw_msg)
            session.commit()  # transaction is committed here
        except:
            session.rollback()  # rolls back the transaction
            raise

    def work(self, session, raw_msg):
        topic, msg = raw_msg['topic'], raw_msg['body']

        for suffix in self.junk_suffixes:
            if topic.endswith(suffix):
                log.debug("Dropping %r", topic)
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

        # If the user has tweaked their preferences on the frontend, then
        # invalidate our entire in-memory cache of the fmn preferences
        # database.
        if '.fmn.' in topic:
            openid = msg['msg']['openid']
            self.refresh_cache(session, openid)

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
                self.refresh_cache(session, openid)

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
        import pika
        connection = pika.BlockingConnection()
        channel = connection.channel()
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
        log.info("Cleaning up FMNConsumer.")
        super(FMNConsumer, self).stop()
