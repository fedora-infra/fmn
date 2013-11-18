# An example fedmsg koji consumer

import moksha.hub.api
import fmn.lib

import datetime
import logging
log = logging.getLogger("fmn")


class ConfirmationProducer(moksha.hub.api.PollingProducer):
    def __init__(self, hub):
        log.debug("ConfirmationProducer initializing")
        self.frequency = hub.config.get(
            'fmn.confirmation_frequency',
            datetime.timedelta(seconds=10))
        super(ConfirmationProducer, self).__init__(hub)
        # Find and save the FMNConsumer instance already created by the hub.
        # We are going to re-use its backends and db session.
        self.sister = self._find_fmn_consumer(self.hub)
        log.debug("ConfirmationProducer initialized")

    def _find_fmn_consumer(self, hub):
        for cons in hub.consumers:
            if 'FMNConsumer' in str(type(cons)):
                return cons

        raise ValueError('FMNConsumer not found by ConfirmationProducer')

    def poll(self):
        # 1) Look for confirmations that need action in the db
        pending = fmn.lib.models.Confirmation.list_pending(self.sister.session)

        # 2) process each one.
        for confirmation in pending:
            log.info("Processing confirmation %r" % confirmation)
            backend = self.sister.backends[confirmation.context.name]
            backend.handle_confirmation(confirmation)

        # 3) clean up any old ones that need to be deleted.
        fmn.lib.models.Confirmation.delete_expired(self.sister.session)
