from fmn.consumer.backends.base import BaseBackend

import logging
log = logging.getLogger("fmn.gcm")

class GCMBackend(BaseBackend):
    def handle(self, recipient, msg):
        log.debug("cloud lololol %r" % recipient)
