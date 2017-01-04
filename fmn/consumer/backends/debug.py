from __future__ import print_function

import datetime

import fedmsg.meta

from fmn.consumer.backends.base import BaseBackend


CONFIRMATION_TEMPLATE = u"""
{username} has requested that notifications be sent to this email address
* To accept, visit this address:
  {acceptance_url}
* Or, to reject you can visit this address:
  {rejection_url}
Alternatively, you can ignore this.  This is an automated message, please
email {support_email} if you have any concerns/issues/abuse.
"""


class DebugBackend(BaseBackend):
    __context_name__ = "debug"

    def __init__(self, *args, **kwargs):
        super(DebugBackend, self).__init__(*args, **kwargs)

    def handle(self, session, recipient, msg, streamline=False):
        topic = msg['topic']
        category = topic.split('.')[3]

        link = fedmsg.meta.msg2link(msg, **self.config) or u''
        content = fedmsg.meta.msg2long_form(msg, **self.config) or u''
        subject = fedmsg.meta.msg2subtitle(msg, **self.config) or u''

        usernames = fedmsg.meta.msg2usernames(msg, **self.config)
        packages = fedmsg.meta.msg2packages(msg, **self.config)

        print('  -- Single message --')
        print('recipient:   ' + str(recipient))
        print('subject:     ' + str(subject))
        print('content:     ' + content + "\n\t" + link)
        print('topic:       ' + str([topic]))
        print('category:    ' + str([category]))
        print('usernames:   ' + str(usernames))
        print('packages:    ' + str(packages))

    def handle_batch(self, session, recipient, messages):
        def _format_line(msg):
            timestamp = datetime.datetime.fromtimestamp(msg['timestamp'])
            link = fedmsg.meta.msg2link(msg, **self.config) or u''
            payload = fedmsg.meta.msg2subtitle(msg, **self.config) or u''

            if recipient.get('verbose', True):
                longform = fedmsg.meta.msg2long_form(msg, **self.config) or u''
                if longform:
                    payload += "\n" + longform

            return timestamp.strftime("%c") + ", " + payload + "\n\t" + link

        n = len(messages)
        subject = u"Fedora Notifications Digest (%i updates)" % n
        summary = u"Digest summary:\n"
        for i, msg in enumerate(messages):
            line = fedmsg.meta.msg2subtitle(msg, **self.config) or u''
            summary += str(i + 1) + ".\t" + line + "\n"

        separator = "\n\n" + "-"*79 + "\n\n"
        if recipient.get('verbose', True):
            content = summary + separator
        else:
            content = u''

        content += separator.join([
            _format_line(msg)
            for msg in messages])

        topics = set([msg['topic'] for msg in messages])
        categories = set([topic.split('.')[3] for topic in topics])

        def squash(items):
            reduce(set.union, items, set())

        usernames = squash([
            fedmsg.meta.msg2usernames(msg, **self.config)
            for msg in messages])
        packages = squash([
            fedmsg.meta.msg2packages(msg, **self.config)
            for msg in messages])

        print('  -- Batch --')
        print('recipient:   ' + str(recipient))
        print('subject:     ' + str(subject))
        print('content:     ' + content)
        print('topic:       ' + str(topics))
        print('category:    ' + str(categories))
        print('usernames:   ' + str(usernames))
        print('packages:    ' + str(packages))

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

        recipient = {
            'user': confirmation.user.openid,
            'email address': confirmation.detail_value,
            'triggered_by_links': False,
        }

        print('  -- Confirmation --')
        print('recipient:   ', recipient)
        print('content:     ', content)
