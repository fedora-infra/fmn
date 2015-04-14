# An example fedmsg koji consumer

import threading
import time
import random

import fedmsg.consumers
import fmn.lib
import fmn.rules.utils
import backends as fmn_backends

from fmn.consumer.util import (
    new_packager,
    new_badges_user,
    get_fas_email,
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

        log.debug("Instantiating FMN backends")
        backend_kwargs = dict(config=self.hub.config)
        self.backends = {
            'email': fmn_backends.EmailBackend(**backend_kwargs),
            'irc': fmn_backends.IRCBackend(**backend_kwargs),
            'android': fmn_backends.GCMBackend(**backend_kwargs),
            #'rss': fmn_backends.RSSBackend,
        }

        # But, disable any of those backends that don't appear explicitly in
        # our config.
        for key, value in self.backends.items():
            if key not in self.hub.config['fmn.backends']:
                del self.backends[key]

        # Also, check that we don't have something enabled that's not explicit
        for key in self.hub.config['fmn.backends']:
            if key not in self.backends:
                raise ValueError("%r in fmn.backends (%r) is invalid" % (
                    key, self.hub.config['fmn.backends']))

        log.debug("Loading rules from fmn.rules")
        self.valid_paths = fmn.lib.load_rules(root="fmn.rules")

        # Initialize our in-memory cache of the FMN preferences database
        self.cached_preferences_lock = threading.Lock()
        self.cached_preferences = None
        session = self.make_session()
        self.refresh_cache(session)
        session.close()

        log.debug("FMNConsumer initialized")

    def refresh_cache(self, session, openid=None):
        log.debug("Acquiring cached_preferences_lock")
        with self.cached_preferences_lock:
            if not openid or self.cached_preferences is None:
                log.info("Loading and caching all preferences for all users")
                self.cached_preferences = fmn.lib.load_preferences(
                    session, self.hub.config, self.valid_paths,
                    cull_disabled=True,
                    cull_backends=['desktop'])
            else:
                log.info("Loading and caching preferences for %r" % openid)
                old_preferences = [p for p in self.cached_preferences
                                   if p['user']['openid'] == openid]
                new_preferences = fmn.lib.load_preferences(
                    session, self.hub.config, self.valid_paths,
                    cull_disabled=True, openid=openid,
                    cull_backends=['desktop'])
                self.cached_preferences.extend(new_preferences)
                for old_preference in old_preferences:
                    self.cached_preferences.remove(old_preference)

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

        # First, make a thread-local copy of our shared cached prefs
        preferences = list(self.cached_preferences)
        # Shuffle it so that not all threads step through the list in the same
        # order.  This should cut down on competition for the dogpile lock when
        # getting pkgdb info at startup.
        random.shuffle(preferences)
        # And do the real work of comparing every rule against the message.
        results = fmn.lib.recipients(preferences, msg,
                                     self.valid_paths, self.hub.config)

        log.debug("Recipients found %i dt %0.2fs %s %s",
                  len(results), time.time() - start,
                  msg['msg_id'], msg['topic'])

        # Let's look at the results of our matching operation and send stuff
        # where we need to.
        for context, recipients in results.items():
            if not recipients:
                continue
            log.debug("  Considering %r with %i recips" % (
                context, len(list(recipients))))
            backend = self.backends[context]
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

        log.debug("Done.  %0.2fs %s %s",
                  time.time() - start, msg['msg_id'], msg['topic'])

    def stop(self):
        log.info("Cleaning up FMNConsumer.")
        for context, backend in self.backends.iteritems():
            backend.stop()
        super(FMNConsumer, self).stop()
