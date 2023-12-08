# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from email.message import EmailMessage

from aiosmtplib import SMTP, SMTPServerDisconnected

from .handler import Handler

log = logging.getLogger(__name__)


class EmailHandler(Handler):
    async def setup(self):
        self._smtp = SMTP(
            hostname=self._config.get("smtp_host", "localhost"),
            port=self._config.get("smtp_port", 25),
        )
        await self._smtp.connect()

    async def stop(self):
        await self._smtp.quit()

    async def handle(self, message):
        # Test with `python -m smtpd -c DebuggingServer -n`
        notif = EmailMessage()
        notif["From"] = self._config["from"]
        for name, value in message["headers"].items():
            notif[name] = value
        body = message["body"]
        if message.get("footer") is not None:
            body = f"{body}\n\n-- \n{message['footer']}"
        notif.set_content(body)
        log.info("Sending email to %s with subject %s", notif["To"], notif["Subject"])
        try:
            await self._smtp.send_message(notif)
        except SMTPServerDisconnected:
            # Reconnect
            log.debug("Reconnecting to the SMTP server")
            self._smtp.close()
            await self._smtp.connect()
            await self._smtp.send_message(notif)
        log.debug("The email was sent")
