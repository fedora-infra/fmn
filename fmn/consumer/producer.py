# An example fedmsg koji consumer

import moksha.hub.api
import fmn.lib

import datetime
import logging
log = logging.getLogger("fmn")


class FMNProducerBase(moksha.hub.api.PollingProducer):
    """ An abstract base class for our other producers. """
    def __init__(self, hub):
        log.debug("%s initializing" % str(type(self)))
        self.frequency = hub.config.get(
            'fmn.confirmation_frequency',
            datetime.timedelta(seconds=10))
        super(FMNProducerBase, self).__init__(hub)
        # Find and save the FMNConsumer instance already created by the hub.
        # We are going to re-use its backends and db session.
        self.sister = self._find_fmn_consumer(self.hub)
        log.debug("%s initialized" % str(type(self)))

    def _find_fmn_consumer(self, hub):
        for cons in hub.consumers:
            if 'FMNConsumer' in str(type(cons)):
                return cons

        raise ValueError('FMNConsumer not found by ConfirmationProducer')

    @property
    def session(self):
        return self.sister.session

    @property
    def backends(self):
        return self.sister.backends


class ConfirmationProducer(FMNProducerBase):
    """ Handle managing the pending confirmations. """

    def poll(self):
        # 1) Look for confirmations that need action in the db
        pending = fmn.lib.models.Confirmation.list_pending(self.session)

        # 2) process each one.
        for confirmation in pending:
            log.info("Processing confirmation %r" % confirmation)
            backend = self.backends[confirmation.context.name]
            backend.handle_confirmation(confirmation)

        # 3) clean up any old ones that need to be deleted.
        fmn.lib.models.Confirmation.delete_expired(self.session)


class DigestProducer(FMNProducerBase):
    """ Handle sending out digests of messages for various contexts. """

    def poll(self):
        # 1) Loop over all preferences in the db
        for pref in fmn.lib.models.Preference.list_batching(self.session):
            # 2) Look for queued messages that need sent by time and count
            earliest = fmn.lib.models.QueuedMessage.earliest_for(
                self.session, pref.user, pref.context)
            count = fmn.lib.models.QueuedMessage.count_for(
                self.session, pref.user, pref.context)
            now = datetime.datetime.utcnow()
            backend = self.backends[pref.context.name]

            # 2.1) Send and dequeue those by time
            if pref.batch_delta >= (now - earliest.created_on):
                queued_messages = fmn.lib.models.QueuedMessage.list_for(
                    self.session, pref.user, pref.context)
                backend.handle_batch(queued_messages)
                for message in queued_messages:
                    message.dequeue(self.session)

            # 2.1) Send and dequeue those by count
            if pref.batch_count >= count:
                queued_messages = fmn.lib.models.QueuedMessage.list_for(
                    self.session, pref.user, pref.context)
                backend.handle_batch(queued_messages)
                for message in queued_messages:
                    message.dequeue(self.session)
