from fmn.consumer.backends.base import BaseBackend


class GCMBackend(BaseBackend):
    def handle(self, recipient, msg):
        self.log.debug("      cloud lololol %r" % recipient)
