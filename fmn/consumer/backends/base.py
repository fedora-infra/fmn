import abc

import logging
import fmn.lib.models


class BaseBackend(object):
    __metaclass__ = abc.ABCMeta
    die = False

    def __init__(self, config, **kwargs):
        self.config = config
        self.log = logging.getLogger("fmn")

    # Some methods that must be implemented by backends.
    @abc.abstractmethod
    def handle(self, session, recipient, msg, streamline=False):
        pass

    @abc.abstractmethod
    def handle_batch(self, session, queued_messages):
        pass

    @abc.abstractmethod
    def handle_confirmation(self, session, confirmation):
        pass

    # Some helper methods for our child classes.
    def context_object(self, session):
        return fmn.lib.models.Context.get(self.__context_name__)

    def preference_for(self, session, detail_value):
        return fmn.lib.models.Preference.by_detail(session, detail_value)

    def disabled_for(self, session, detail_value):
        pref = self.preference_for(session, detail_value)

        if not pref:
            return False

        return not pref.enabled

    def enable(self, session, detail_value):
        self.preference_for(session, detail_value).set_enabled(session, True)

    def disable(self, session, detail_value):
        self.preference_for(session, detail_value).set_enabled(session, False)

    def stop(self):
        self.die = True
