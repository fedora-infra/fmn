# This file is part of the FMN project.
# Copyright (C) 2017 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
from .base import BaseBackend

from kitchen.text.converters import to_bytes

import email
import logging

from twisted.internet import defer
from twisted.mail import smtp

from fmn.lib import models
from fmn.util import get_fas_email

_log = logging.getLogger(__name__)


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
    """Backend for handling email messages for FMN."""
    __context_name__ = "email"

    def __init__(self, *args, **kwargs):
        super(EmailBackend, self).__init__(*args, **kwargs)
        self.mailserver = self.config['fmn.email.mailserver']
        if ':' in self.mailserver:
            self.host, self.port = self.mailserver.split(':')
        else:
            self.host, self.port = self.mailserver, 25
        self.port = int(self.port)
        self.from_address = self.config['fmn.email.from_address']

    @defer.inlineCallbacks
    def deliver(self, formatted_message, recipient, raw_fedmsg):
        """
        Deliver a message to the recipient.

        Args:
            formatted_message (str): The formatted message that is ready for delivery
                to the user. It has been formatted according to the user's preferences.
            recipient (dict): The recipient of the message.
            raw_fedmsg (dict): The original fedmsg that was used to produce the formatted
                message.
        """
        try:
            # TODO handle the mail server being down gracefully
            yield smtp.sendmail(
                self.host,
                to_bytes(self.from_address),
                [to_bytes(recipient['email address'])],
                formatted_message,
                port=self.port,
            )
            _log.info('Email successfully delivered to %s', recipient['email address'])
        except smtp.SMTPBadRcpt as e:
            _log.info('Failed to email %s: %s', recipient['email address'], str(e))
            self.handle_bad_email_address(recipient)

    def handle_confirmation(self, session, confirmation):
        """
        Send a confirmation email to new user emails with a confirmation link.

        Args:
            session (sqlalchemy.orm.session.Session): The session to use.
            confirmation (models.Confirmation): The confirmation database entry.
        """
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
        email_message = email.Message.Message()
        email_message.add_header('To', recipient['email address'])
        email_message.add_header('From', self.from_address)
        # Although this is a non-standard header and RFC 2076 discourages it, some
        # old clients don't honour RFC 3834 and will auto-respond unless this is set.
        email_message.add_header('Precendence', 'Bulk')
        # Mark this mail as auto-generated so auto-responders don't respond; see RFC 3834
        email_message.add_header('Auto-Submitted', 'auto-generated')
        email_message.add_header('Subject', subject)
        email_message.set_payload(content)

        self.deliver(email_message.as_string(), recipient, {})

    def handle_bad_email_address(self, recipient):
        """ Handle a bad email address.
        1) Look up the account in FAS.  Use their email there if possible.
        2) If not, then just disable their account.

        See https://github.com/fedora-infra/fmn/issues/28
        """
        session = models.Session()
        address = recipient['email address']
        user = recipient['user']
        _log.warning("Dealing with bad email %s, %s" % (address, user))
        pref = self.preference_for(session, address)
        if address.endswith('@fedoraproject.org'):
            fas_email = get_fas_email(self.config, user)
            _log.info("Got fas email as %r " % fas_email)
            if fas_email != address:
                pref.delete_details(session, address)
                pref.update_details(session, fas_email)
            else:
                _log.warning("Disabling %s for good..." % user)
                pref.set_enabled(session, False)
        else:
            _log.warning("Disabling %s for good..." % user)
            pref.set_enabled(session, False)
        session.commit()
