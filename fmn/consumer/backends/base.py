import logging

class BaseBackend(object):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger("fmn")

    def handle(self, recipient, msg):
        raise NotImplementedError("BaseBackend must be extended")
