# An example fedmsg koji consumer
import datetime
import logging

import fmn.lib


log = logging.getLogger("fmn")


def total_seconds(dt):
    """ Take a datetime.timedelta object and return the total seconds.

    dt.total_seconds() exists in the python 2.7 stdlib, but not in python 2.6.
    """
    return dt.days * 24 * 60 * 60 + dt.seconds + dt.microseconds / 1000000.0


class FMNProducerBase(object):
    """ An abstract base class for our other producers. """
    def __init__(self, session, backends):
        log.debug("%s initializing" % str(type(self)))
        self.session = session
        self.backends = backends
        log.debug("%s initialized" % str(type(self)))


class ConfirmationProducer(FMNProducerBase):
    """ Handle managing the pending confirmations. """

    def work(self):
        # 1) Look for confirmations that need action in the db
        pending = fmn.lib.models.Confirmation.list_pending(self.session)

        # 2) process each one.
        for confirmation in pending:
            log.info("Processing confirmation %r" % confirmation)

            if confirmation.context.name not in self.backends:
                return

            backend = self.backends[confirmation.context.name]
            backend.handle_confirmation(self.session, confirmation)

        # 3) clean up any old ones that need to be deleted.
        fmn.lib.models.Confirmation.delete_expired(self.session)


class DigestProducer(FMNProducerBase):
    """ Handle sending out digests of messages for various contexts. """

    def work(self):
        # 1) Loop over all preferences in the db
        for pref in fmn.lib.models.Preference.list_batching(self.session):

            if pref.context.name not in self.backends:
                log.error('Unknown backend in pref: %s' % pref)
                continue

            # 2) Look for queued messages that need sent by time and count
            count = fmn.lib.models.QueuedMessage.count_for(
                self.session, pref.user, pref.context)
            if not count:
                continue
            earliest = fmn.lib.models.QueuedMessage.earliest_for(
                self.session, pref.user, pref.context)
            now = datetime.datetime.utcnow()
            delta = now - earliest.created_on
            backend = self.backends[pref.context.name]

            # 2.1) Send and dequeue those by time
            if pref.batch_delta is not None:
                if pref.batch_delta <= total_seconds(delta):
                    log.info("Sending digest for %r per time delta" % pref)
                    self.manage_batch(self.session, backend, pref)
                    continue

            # 2.1) Send and dequeue those by count
            if pref.batch_count is not None:
                if pref.batch_count <= count:
                    log.info("Sending digest for %r per msg count" % pref)
                    self.manage_batch(self.session, backend, pref)
                    continue

    @staticmethod
    def manage_batch(session, backend, pref):
        name = pref.context.detail_name
        recipients = [{
            name: value.value,
            'user': pref.user.openid,
            'markup_messages': pref.markup_messages,
            'triggered_by_links': pref.triggered_by_links,
            'shorten_links': pref.shorten_links,
        } for value in pref.detail_values]

        queued_messages = fmn.lib.models.QueuedMessage.list_for(
            session, pref.user, pref.context)

        if queued_messages:
            log.info("* Found %r queued messages" % len(queued_messages))

        for recipient in recipients:

            # If the preference is disabled, then drop all those queued
            # messages.
            if not pref.enabled:
                log.info("* Pref %r inactive.  Dropping messages." % pref)
                continue

            # If there's only a single message, then send it in "the usual way"
            # See https://github.com/fedora-infra/fmn/issues/91
            if len(queued_messages) == 1:
                msg = queued_messages[0].message
                backend.handle(session, recipient, msg, streamline=True)
            else:
                # Otherwise, send it as a batch/digest
                backend.handle_batch(session, recipient,
                                     [q.message for q in queued_messages])

        for message in queued_messages:
            message.dequeue(session)
