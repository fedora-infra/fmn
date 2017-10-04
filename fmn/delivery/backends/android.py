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
import fmn.lib.models
from .base import BaseBackend

import requests
import json


class GCMBackend(BaseBackend):
    __context_name__ = "android"

    def __init__(self, *args, **kwargs):
        super(GCMBackend, self).__init__(*args, **kwargs)
        self.post_url = self.config['fmn.gcm.post_url']
        self.api_key = self.config['fmn.gcm.api_key']

    def _send_notification(self, sess, registration_id, data):
        '''Immediately send a notification to a device. This does **NOT** check
           whether or not the user has notifications enabled. The calling method
           **MUST** do this itself.'''

        # Extra data that applies to all messages goes here. Try to keep it
        # short to save users bandwidth!
        data['fmn_base_url'] = self.config['fmn.base_url']

        headers = {
            'Authorization': 'key=%s' % self.api_key,
            'content-type': 'application/json',
        }

        body = {
            'registration_ids': [registration_id],
            'data': data,
        }

        response = requests.post(
            self.post_url,
            data=json.dumps(body),
            headers=headers)

        self.log.debug(" * got %r %r" % (response.status_code, response.text))

        j = response.json()

        if j.get("message_id") and j.get("message_id").get("registration_id"):
            self.log.debug("   * Was informed by Google that the " +
                           " registration id is old. Updating.")

            pref = fmn.lib.models.Preference.by_detail(sess, registration_id)
            pref.update_details(sess, j.get("message_id").get("registration_id"))

    def handle(self, session, recipient, msg, streamline=False):
        self.log.debug("Notifying via gcm/android %r" % recipient)

        if 'registration id' not in recipient:
            self.log.warning("No registration id found.  Bailing.")
            return

        if self.disabled_for(detail_value=recipient['registration id']):
            self.log.debug("Messages stopped for %r, not sending." % recipient)
            return

        self._send_notification(session, recipient['registration id'], msg)

    def handle_batch(self, session, recipient, messages):
        raise NotImplementedError()

    def handle_confirmation(self, session, confirmation):
        confirmation.set_status(session, 'valid')

        msg = {
            "title": "Fedora Notifications Confirmation",
            "message": "Hi there! Please confirm that you would like to " +
                       "receive Fedora related notifications.",
            "secret": confirmation.secret
        }

        self._send_notification(session, confirmation.detail_value, msg)
