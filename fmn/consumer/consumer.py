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

        log.debug("Loading rules from fmn.rules")
        self.valid_paths = fmn.lib.load_rules(root="fmn.rules")

        log.debug("FMNConsumer initialized")

    def consume(self, raw_msg):
        topic, msg = raw_msg['topic'], raw_msg['body']

        log.debug("Received topic %r" % topic)

        results = fmn.lib.recipients(self.session, self.hub.config,
                                     self.valid_paths, msg)

        for context, recipients in results.items():
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
