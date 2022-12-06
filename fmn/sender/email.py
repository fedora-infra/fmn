import logging
from email.message import EmailMessage

from aiosmtplib import SMTP

from .handler import Handler

_log = logging.getLogger(__name__)


class EmailHandler(Handler):
    async def setup(self):
        self._smtp = SMTP(
            self._config.get("smtp_host", "localhost"), self._config.get("smtp_port", 25)
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
        notif.set_content(message["body"])
        _log.info(f"Sending email to {notif['To']} with subject {notif['Subject']}")
        await self._smtp.send_message(notif)
