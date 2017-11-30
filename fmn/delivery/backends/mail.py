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

import logging

from twisted.internet import defer
from twisted.mail import smtp

from fmn.lib import models
from fmn.util import get_fas_email

_log = logging.getLogger(__name__)

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
                formatted_message.encode('utf-8'),
                port=self.port,
            )
            _log.info('Email successfully delivered to %s', recipient['email address'])
        except smtp.SMTPClientError as e:
            _log.info('Failed to email %s: %s', recipient['email address'], str(e))
            if e.code == 550:
                self.handle_bad_email_address(recipient)
            else:
                raise

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
