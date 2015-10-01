from fmn.consumer.backends.base import BaseBackend
import fedmsg.meta

from kitchen.text.converters import to_bytes, to_unicode

import datetime
import smtplib
import email
import time

from fmn.consumer.util import get_fas_email


CONFIRMATION_TEMPLATE = u"""
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
{base_url}{user}/email/{filter_id}
"""


class EmailBackend(BaseBackend):
    __context_name__ = "email"

    def __init__(self, *args, **kwargs):
        super(EmailBackend, self).__init__(*args, **kwargs)
        self.mailserver = self.config['fmn.email.mailserver']
        self.from_address = self.config['fmn.email.from_address']


    def _get_mailserver(self, address, tries=0):
        """ Connect to our mailserver, but retry a few times if we fail. """
        try:
            # This usually just works
            return smtplib.SMTP(self, address)
        except Exception:
            # However sometimes we get a gaierror (getaddrinfo error)
            # Give up if we tried and tried
            if tries > 3:
                raise
            # Otherwise, try again after sleeping for a moment.
            msg = "Failed in getaddrinfo for %r.  Try #%i." % (address, tries)
            self.log.warn(msg)
            time.sleep(0.5)
            return self._get_mailserver(self, address, tries + 1)

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

        triggered_by = recipient['triggered_by_links']
        if 'filter_id' in recipient and 'user' in recipient and triggered_by:
            base_url = self.config['fmn.base_url']
            footer = reason.format(base_url=base_url, **recipient) + footer

        if footer:
            content += u'\n\n--\n{0}'.format(footer.strip())

        email_message.set_payload(to_bytes(content), 'utf-8')

        # Explicitly declare encoding, but remove the transfer encoding
        # https://github.com/fedora-infra/fmn/issues/94
        email_message.set_charset('utf-8')

        server = self._get_mailserver(self.mailserver)
        try:
            server.sendmail(
                to_bytes(self.from_address),
                [to_bytes(recipient['email address'])],
                to_bytes(email_message.as_string()),
            )
        except smtplib.SMTPRecipientsRefused:
            self.handle_bad_email_address(session, recipient)
        except:
            self.log.info("%r" % email_message.as_string())
            raise
        finally:
            server.quit()
        self.log.debug("Email sent")

    def handle(self, session, recipient, msg, streamline=False):
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
            payload = fedmsg.meta.msg2subtitle(msg, **self.config) or u''

            if recipient.get('verbose', True):
                longform = fedmsg.meta.msg2long_form(msg, **self.config) or u''
                if longform:
                    payload += "\n" + longform

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

        template = self.config.get('fmn.mail_confirmation_template',
                                   CONFIRMATION_TEMPLATE)
        content = template.format(
            acceptance_url=acceptance_url,
            rejection_url=rejection_url,
            support_email=self.config['fmn.support_email'],
            username=confirmation.openid,
        ).strip()
        subject = u'Confirm notification email'

        recipient = {
            'user': confirmation.user.openid,
            'email address': confirmation.detail_value,
            'triggered_by_links': False,
        }

        self.send_mail(session, recipient, subject, content)

    def handle_bad_email_address(self, session, recipient):
        """ Handle a bad email address.
        1) Look up the account in FAS.  Use their email there if possible.
        2) If not, then just disable their account.

        See https://github.com/fedora-infra/fmn/issues/28
        """

        address = recipient['email address']
        user = recipient['user']
        self.log.warning("Dealing with bad email %s, %s" % (address, user))
        pref = self.preference_for(session, address)
        if address.endswith('@fedoraproject.org'):
            fas_email = get_fas_email(self.config, user)
            self.log.info("Got fas email as %r " % fas_email)
            if fas_email != address:
                pref.delete_details(session, address)
                pref.update_details(session, fas_email)
            else:
                self.log.warning("Disabling %s for good..." % user)
                pref.set_enabled(session, False)
        else:
            self.log.warning("Disabling %s for good..." % user)
            pref.set_enabled(session, False)
