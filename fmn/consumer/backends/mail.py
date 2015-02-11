from fmn.consumer.backends.base import BaseBackend
import fedmsg.meta

from kitchen.text.converters import to_bytes, to_unicode

import datetime
import smtplib
import email


confirmation_template = u"""
{username} has requested that notifications be sent to this email address
* To accept, visit this address:
  {acceptance_url}
* Or, to reject you can visit this address:
  {rejection_url}
Alternatively, you can ignore this.  This is an automated message, please
email {support_email} if you have any concerns/issues/abuse.
"""

reason = u"""
You received this message due to your preference settings at
{base_url}/{user}/email/{filter_id}
"""


class EmailBackend(BaseBackend):
    __context_name__ = "email"

    def __init__(self, *args, **kwargs):
        super(EmailBackend, self).__init__(*args, **kwargs)
        self.mailserver = self.config['fmn.email.mailserver']
        self.from_address = self.config['fmn.email.from_address']

    def send_mail(self, session, recipient, subject, content,
                  topics=None, categories=None, usernames=None, packages=None):
        self.log.debug("Sending email")

        if 'email address' not in recipient:
            self.log.warning("No email address found.  Bailing.")
            return

        if self.disabled_for(session, detail_value=recipient['email address']):
            self.log.debug("Messages stopped for %r, not sending." % recipient)
            return

        email_message = email.Message.Message()
        email_message.add_header('To', to_bytes(recipient['email address']))
        email_message.add_header('From', to_bytes(self.from_address))

        # Assemble a menagerie of possibly useful headers
        for topic in topics or []:
            email_message.add_header('X-Fedmsg-Topic', to_bytes(topic))
        for category in categories or []:
            email_message.add_header('X-Fedmsg-Category', to_bytes(category))
        for username in usernames or []:
            email_message.add_header('X-Fedmsg-Username', to_bytes(username))
        for package in packages or []:
            email_message.add_header('X-Fedmsg-Package', to_bytes(package))

        subject_prefix = self.config.get('fmn.email.subject_prefix', '')
        if subject_prefix:
            subject = '{0} {1}'.format(
                subject_prefix.strip(), subject.strip())

        email_message.add_header('Subject', to_bytes(subject))

        # Since we do simple text email, adding the footer to the content
        # before setting the payload.
        footer = to_unicode(self.config.get('fmn.email.footer', ''))

        if 'filter_id' in recipient and 'user' in recipient:
            base_url = self.config['fmn.base_url']
            footer = reason.format(base_url=base_url, **recipient) + footer

        if footer:
            content += u'\n\n--\n{0}'.format(footer.strip())

        email_message.set_payload(to_bytes(content))

        server = smtplib.SMTP(self.mailserver)
        try:
            server.sendmail(
                to_bytes(self.from_address),
                [to_bytes(recipient['email address'])],
                to_bytes(email_message.as_string()),
            )
        except:
            self.log.info("%r" % email_message.as_string())
            raise
        finally:
            server.quit()
        self.log.debug("Email sent")

    def handle(self, session, recipient, msg):
        topic = msg['topic']
        category = topic.split('.')[3]

        link = fedmsg.meta.msg2link(msg, **self.config) or u''
        content = fedmsg.meta.msg2long_form(msg, **self.config) or u''
        subject = fedmsg.meta.msg2subtitle(msg, **self.config) or u''

        usernames = fedmsg.meta.msg2usernames(msg, **self.config)
        packages = fedmsg.meta.msg2packages(msg, **self.config)

        self.send_mail(session, recipient, subject, content + "\n\t" + link,
                       [topic], [category], usernames, packages)

    def handle_batch(self, session, recipient, queued_messages):
        def _format_line(msg):
            timestamp = datetime.datetime.fromtimestamp(msg['timestamp'])
            link = fedmsg.meta.msg2link(msg, **self.config) or u''
            payload = fedmsg.meta.msg2long_form(msg, **self.config) or u''
            return timestamp.strftime("%c") + ", " + payload + "\n\t" + link

        n = len(queued_messages)
        subject = u"Fedora Notifications Digest (%i updates)" % n
        content = "\n".join([
            _format_line(queued_message.message)
            for queued_message in queued_messages])

        topics = set([q.message['topic'] for q in queued_messages])
        categories = set([topic.split('.')[3] for topic in topics])

        squash = lambda items: reduce(set.union, items, set())
        usernames = squash([
            fedmsg.meta.msg2usernames(q.message, **self.config)
            for q in queued_messages])
        packages = squash([
            fedmsg.meta.msg2packages(q.message, **self.config)
            for q in queued_messages])

        self.send_mail(session, recipient, subject, content,
                       topics, categories, usernames, packages)


    def handle_confirmation(self, session, confirmation):
        confirmation.set_status(session, 'valid')
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
        subject = u'Confirm notification email'

        recipient = {'email address': confirmation.detail_value}

        self.send_mail(session, recipient, subject, content)
