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

        if 'email address' not in recipient:
            self.log.warning("No email address found.  Bailing.")
            return

        email_message = email.Message.Message()
        email_message.add_header('To', recipient['email address'])
        email_message.add_header('From', self.from_address)

        subject = fedmsg.meta.msg2subtitle(msg, **self.config)
        email_message.add_header('Subject', subject)

        content = fedmsg.meta.msg2repr(msg, **self.config)

        # Since we do simple text email, adding the footer to the content
        # before setting the payload.
        footer = self.config.get('fmn.email.footer', None)
        if footer:
            content += '/n--/n {0}'.format(footer)

        email_message.set_payload(content)

        self.server.sendmail(
            self.from_address,
            [recipient['email address']],
            email_message.as_string(),
        )
