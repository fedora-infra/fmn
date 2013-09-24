# An example fedmsg koji consumer

import fedmsg.consumers
import fmn.lib
import backends as fmn_backends

from pprint import pprint

import logging
log = logging.getLogger("fmn")

class FMNConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.prod.*'
    config_key = 'fmn.consumer.enabled'

    backends = {
        'email': fmn_backends.EmailBackend,
        'irc': fmn_backends.IRCBackend,
        'gcm': fmn_backends.GCMBackend,
        #'rss': fmn_backends.RSSBackend,
    }

    def __init__(self, *args, **kwargs):
        log.debug("Trying to set up FMNConsumer")
        super(FMNConsumer, self).__init__(*args, **kwargs)

        uri = self.hub.config.get('fmn.sqlalchemy.uri', None)

        if not uri:
            raise ValueError('fmn.sqlalchemy.uri must be present')

        self.session = fmn.lib.models.init(uri)
        log.debug("FMNConsumer initialized")


    def consume(self, raw_msg):
        topic, msg = raw_msg['topic'], raw_msg['body']
        log.debug("Received topic %r" % topic)
        results = fmn.lib.recipients(self.session, msg)
        log.debug("Found %i results" % len(results))
        for context, recipients in results.items():
            log.debug("Considering %r with %i recips" % (context, len(list(recipients))))
            backend = self.backends[context]
            for recipient in recipients:
                backend.handle(recipient, message)

