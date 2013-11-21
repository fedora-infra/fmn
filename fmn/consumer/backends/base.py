import logging


class BaseBackend(object):
    def __init__(self, config, session, **kwargs):
        self.config = config
        self.session = session
        self.log = logging.getLogger("fmn")

    def handle(self, recipient, msg):
        raise NotImplementedError("BaseBackend must be extended")

    def handle_batch(self, session, queued_messages):
        raise NotImplementedError("BaseBackend must be extended")

    def handle_confirmation(self, session, confirmation):
        raise NotImplementedError("BaseBackend must be extended")

