from fmn.consumer.backends.base import BaseBackend
import fedmsg.meta

import smtplib
import email


class EmailBackend(BaseBackend):

    def __init__(self, *args, **kwargs):
        super(EmailBackend, self).__init__(*args, **kwargs)
        self.mailserver = self.config['fmn.email.mailserver']
        self.from_address = self.config['fmn.email.from_address']
        self.server = smtplib.SMTP(self.mailserver)

    def handle(self, recipient, msg):
        self.log.debug("Sending email")
        email_message = email.Message.Message()

        email_message.add_header('To', recipient['address'])
        email_message.add_header('From', self.from_address)

        subject = fedmsg.meta.msg2subtitle(msg, **self.config)
        email_message.add_header('Subject', subject)

        content = fedmsg.meta.msg2repr(msg, **self.config)
        email_message.set_payload(content)

        # TODO -- add a customizable footer indicating where the user can go to
        # change their preferences/unsubscribe.

        self.server.sendmail(
            self.from_address,
            [recipient['address']],
            email_message.as_string(),
        )
