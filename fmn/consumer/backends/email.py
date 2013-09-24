from fmn.consumer.backends.base import BaseBackend

import logging
log = logging.getLogger("fmn.email")


class EmailBackend(BaseBackend):
    def handle(self, recipient, msg):
        log.debug("Sending email lolololol %r" % recipient)
