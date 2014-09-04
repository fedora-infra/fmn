# An example fedmsg koji consumer

import threading

import fedmsg.consumers
import fmn.lib
import fmn.rules.utils
import backends as fmn_backends

import logging
log = logging.getLogger("fmn")


class FMNConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.*'
    config_key = 'fmn.consumer.enabled'

    def __init__(self, *args, **kwargs):
        log.debug("FMNConsumer initializing")
        super(FMNConsumer, self).__init__(*args, **kwargs)

        self.uri = self.hub.config.get('fmn.sqlalchemy.uri', None)

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

        self.cached_preferences = None
        self.cached_preferences_lock = threading.Lock()

        log.debug("FMNConsumer initialized")

    def refresh_cache(self, session, topic=None, msg=None):
        log.info("Loading and caching preferences")
        with self.cached_preferences_lock:
            self.cached_preferences = fmn.lib.load_preferences(
                session, self.hub.config, self.valid_paths, cull_disabled=True)

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

        log.debug("FMNConsumer received topic %r" % topic)

        # First, do some cache management.  This can be confusing because there
        # are two different caches, with two different mechanisms, storing two
        # different kinds of data.  The first is a simple python dict that
        # contains the 'preferences' from the fmn database.  The second is a
        # dogpile.cache (potentially stored in memcached, but configurable from
        # /etc/fedmsg.d/).  The dogpile.cache cache stores pkgdb2
        # package-ownership relations.  Both caches are held for a very long
        # time and update themselves dynamically here.
        #
        # If the user has tweaked their preferences on the frontend, then
        # invalidate our entire in-memory cache of the fmn preferences
        # database.
        if '.fmn.' in topic or not self.cached_preferences:
            self.refresh_cache(session, topic, msg)

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

        # Create a local account with all the default rules if an user is added
        # to the `packager` group in FAS
        if '.fas.group.member.sponsor' in topic:
            group = msg['msg']['group']
            if group == 'packager':
                usernames = fedmsg.meta.msg2usernames(msg, **self.hub.config)
                for username in usernames:
                    openid='%s.id.fedoraproject.org' % username
                    openid_url = 'https://%s.id.fedoraproject.org' % username
                    email = '%s@fedoraproject.org' % username
                    user = fmn.lib.models.User.get_or_create(
                        session, openid=openid, openid_url=openid_url,
                        create_defaults=True, detail_values=dict(email=email),
                    )
                    session.add(user)
                session.commit()
                self.refresh_cache(session, topic, msg)

        # Do the same invalidation trick for fas group membership changes.
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
        results = fmn.lib.recipients(self.cached_preferences, msg,
                                     self.valid_paths, self.hub.config)

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

    def stop(self):
        log.info("Cleaning up FMNConsumer.")
        for context, backend in self.backends.iteritems():
            backend.stop()
        super(FMNConsumer, self).stop()
