import logging
import fmn.lib.models


class BaseBackend(object):
    def __init__(self, config, session, **kwargs):
        self.config = config
        self.session = session
        self.log = logging.getLogger("fmn")
        self.context_object = fmn.lib.models.Context.get(
            session, self.__context_name__)

    # Some methods that must be implemented by backends.
    def handle(self, recipient, msg):
        raise NotImplementedError("BaseBackend must be extended")

    def handle_batch(self, session, queued_messages):
        raise NotImplementedError("BaseBackend must be extended")

    def handle_confirmation(self, session, confirmation):
        raise NotImplementedError("BaseBackend must be extended")

    # Some helper methods for our child classes.
    def preference_for(self, detail_value):
        return fmn.lib.models.Preference.by_detail(self.session, detail_value)

    def disabled_for(self, detail_value):
        pref = self.preference_for(detail_value)

        if not pref:
            return False

        return not pref.enabled

    def enable(self, detail_value):
        self.preference_for(detail_value).set_enabled(self.session, True)

    def disable(self, detail_value):
        self.preference_for(detail_value).set_enabled(self.session, False)
