class BaseBackend(object):
    def handle(self, recipient, msg):
        raise NotImplementedError("BaseBackend must be extended")
