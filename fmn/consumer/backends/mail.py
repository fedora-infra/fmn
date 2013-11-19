from fmn.consumer.backends.base import BaseBackend
import fedmsg.meta

import smtplib
import email


confirmation_template = """
{username} has requested that notifications be sent to this email address
* To accept, visit this address:
  {acceptance_url}
* Or, to reject you can visit this address:
  {rejection_url}
Alternatively, you can ignore this.  This is an automated message, please
email {support_email} if you have any concerns/issues/abuse.
"""

class EmailBackend(BaseBackend):

    def __init__(self, *args, **kwargs):
        super(EmailBackend, self).__init__(*args, **kwargs)
        self.mailserver = self.config['fmn.email.mailserver']
        self.from_address = self.config['fmn.email.from_address']
        self.server = smtplib.SMTP(self.mailserver)

    def send_mail(self, recipient, content):
        self.log.debug("Sending email")

        if 'email address' not in recipient:
            self.log.warning("No email address found.  Bailing.")
            return

        email_message = email.Message.Message()
        email_message.add_header('To', recipient['email address'])
        email_message.add_header('From', self.from_address)

        subject = fedmsg.meta.msg2subtitle(msg, **self.config)
        email_message.add_header('Subject', subject)

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

    def handle(self, recipient, msg):
        content = fedmsg.meta.msg2repr(msg, **self.config)

        self.send_mail(recipient, content)

    def handle_confirmation(self, session, confirmation):
        confirmations = fmn.lib.models.Confirmation.by_detail(
            self.session, context="email", recipient['email address'])

        for confirmation in confirmations:
            lines = confirmation_template.format(
                acceptance_url=acceptance_url,
                rejection_url=rejection_url,
                support_email=self.config['fmn.support_email'],
                username=confirmation.user_name,
            ).strip()

            recipient = {'email address' : }

            self.send_mail(recipient, lines)
