import logging


class BaseBackend(object):
    def __init__(self, config, **kwargs):
        self.config = config
        self.log = logging.getLogger("fmn")

    def handle(self, recipient, msg):
        raise NotImplementedError("BaseBackend must be extended")
