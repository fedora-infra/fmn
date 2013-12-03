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

reason = """
You received this message due to your preference settings at
{base_url}/{user}/email/{filter}
"""


class EmailBackend(BaseBackend):
    __context_name__ = "email"

    def __init__(self, *args, **kwargs):
        super(EmailBackend, self).__init__(*args, **kwargs)
        self.mailserver = self.config['fmn.email.mailserver']
        self.from_address = self.config['fmn.email.from_address']

    def send_mail(self, recipient, subject, content):
        self.log.debug("Sending email")

        if 'email address' not in recipient:
            self.log.warning("No email address found.  Bailing.")
            return

        if self.disabled_for(detail_value=recipient['email address']):
            self.log.debug("Messages stopped for %r, not sending." % nickname)
            return

        email_message = email.Message.Message()
        email_message.add_header('To', recipient['email address'])
        email_message.add_header('From', self.from_address)

        subject_prefix = self.config.get('fmn.email.subject_prefix', '')
        if subject_prefix:
            subject = '{0} {1}'.format(
                subject_prefix.strip(), subject.strip())

        email_message.add_header('Subject', subject)

        # Since we do simple text email, adding the footer to the content
        # before setting the payload.
        footer = self.config.get('fmn.email.footer', '')

        if 'filter' in recipient and 'user' in recipient:
            base_url = self.config['fmn.base_url']
            footer = reason.format(base_url=base_url, **recipient) + footer

        if footer:
            content += '\n\n--\n{0}'.format(footer.strip())

        email_message.set_payload(content)

        server = smtplib.SMTP(self.mailserver)
        server.sendmail(
            self.from_address.encode('utf-8'),
            [recipient['email address'].encode('utf-8')],
            email_message.as_string().encode('utf-8'),
        )
        server.quit()
        self.log.debug("Email sent")

    def handle(self, recipient, msg):
        content = fedmsg.meta.msg2repr(msg, **self.config)
        subject = fedmsg.meta.msg2subtitle(msg, **self.config)

        self.send_mail(recipient, subject, content)

    def handle_batch(self, recipient, queued_messages):
        subject = "Fedora Notifications Digest"
        content = "\n".join([
            fedmsg.meta.msg2repr(queued_message.msg, **self.config)
            for queued_message in queued_messages])

        self.send_mail(recipient, subject, content)

    def handle_confirmation(self, confirmation):
        confirmation.set_status(self.session, 'valid')
        acceptance_url = self.config['fmn.acceptance_url'].format(
            secret=confirmation.secret)
        rejection_url = self.config['fmn.rejection_url'].format(
            secret=confirmation.secret)

        content = confirmation_template.format(
            acceptance_url=acceptance_url,
            rejection_url=rejection_url,
            support_email=self.config['fmn.support_email'],
            username=confirmation.openid,
        ).strip()
        subject = 'Confirm notification email'

        recipient = {'email address': confirmation.detail_value}

        self.send_mail(recipient, subject, content)
