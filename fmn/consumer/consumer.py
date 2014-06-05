# An example fedmsg koji consumer

import fedmsg.consumers
import fmn.lib
import backends as fmn_backends

from pprint import pprint

import logging
log = logging.getLogger("fmn")


class FMNConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.*'
    config_key = 'fmn.consumer.enabled'

    def __init__(self, *args, **kwargs):
        log.debug("FMNConsumer initializing")
        super(FMNConsumer, self).__init__(*args, **kwargs)

        uri = self.hub.config.get('fmn.sqlalchemy.uri', None)

        if not uri:
            raise ValueError('fmn.sqlalchemy.uri must be present')

        log.debug("Setting up DB session")
        self.session = fmn.lib.models.init(uri)

        log.debug("Instantiating FMN backends")
        backend_kwargs = dict(config=self.hub.config, session=self.session)
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

        self.refresh_cache()

        log.debug("FMNConsumer initialized")

    def refresh_cache(self, topic=None, msg=None):
        log.debug("Loading and caching preferences")
        self.cached_preferences = fmn.lib.load_preferences(
            self.session, self.hub.config, self.valid_paths)

    def consume(self, raw_msg):
        topic, msg = raw_msg['topic'], raw_msg['body']

        log.debug("FMNConsumer received topic %r" % topic)

        if '.fmn.' in topic:
            self.refresh_cache(topic, msg)

        results = fmn.lib.recipients(self.cached_preferences, msg,
                                     self.valid_paths, self.hub.config)

        for context, recipients in results.items():
            if not recipients:
                continue
            log.debug("  Considering %r with %i recips" % (
                context, len(list(recipients))))
            backend = self.backends[context]
            for recipient in recipients:
                user = recipient['user']
                pref = fmn.lib.models.Preference.load(
                    self.session, user, context)

                if not pref.should_batch:
                    log.debug("    Calling backend %r with %r" % (
                        backend, recipient))
                    backend.handle(recipient, msg)
                else:
                    log.debug("    Queueing msg for digest")
                    fmn.lib.models.QueuedMessage.enqueue(
                        self.session, user, context, msg)

    def stop(self):
        log.info("Cleaning up FMNConsumer.")
        for context, backend in self.backends.iteritems():
            backend.stop()
        super(FMNConsumer, self).stop()
