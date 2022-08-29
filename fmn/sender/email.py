import smtplib
from email.message import EmailMessage

from .handler import Handler


class EmailHandler(Handler):
    def setup(self):
        self._smtp = smtplib.SMTP(
            host=self._config.get("smtp_host", "localhost"), port=self._config("smtp_port", 25)
        )

    def stop(self):
        self._smtp.quit()

    def handle(self, message):
        notif = EmailMessage()
        notif["From"] = self._config["from"]
        for name, value in message["headers"].items():
            notif[name] = value
        notif.set_content(message["body"])

        self._smtp.send_message(notif)
