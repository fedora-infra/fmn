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

from __future__ import print_function

from .base import BaseBackend


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

    def deliver(self, formatted_message, recipient, raw_fedmsg):
        print(formatted_message)

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
