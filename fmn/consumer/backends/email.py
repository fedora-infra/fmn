from fmn.consumer.backends.base import BaseBackend


class EmailBackend(BaseBackend):
    def handle(self, recipient, msg):
        self.log.debug("      Sending email lolololol %r" % recipient)
