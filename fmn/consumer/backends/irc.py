from fmn.consumer.backends.base import BaseBackend

class IRCBackend(BaseBackend):
    def handle(self, recipient, msg):
        self.log.debug("      Privmsging on irc lololol %r" % recipient)
