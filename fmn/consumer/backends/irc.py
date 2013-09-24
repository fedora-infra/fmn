from fmn.consumer.backends.base import BaseBackend

import logging
log = logging.getLogger("fmn.irc")

class IRCBackend(BaseBackend):
    def handle(self, recipient, msg):
        log.debug("Privmsging on irc lololol %r" % recipient)
