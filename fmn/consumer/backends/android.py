from fmn.consumer.backends.base import BaseBackend

import requests
import json


class GCMBackend(BaseBackend):
    __context_name__ = "android"

    def __init__(self, *args, **kwargs):
        super(GCMBackend, self).__init__(*args, **kwargs)
        self.post_url = self.config['fmn.gcm.post_url']
        self.api_key = self.config['fmn.gcm.api_key']

    def _send_notification(self, registration_id, data):
      '''Immediately send a notification to a device. This does **NOT** check
         whether or not the user has notifications enabled. The calling method
         **MUST** do this itself.'''

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


    def handle(self, recipient, msg):
        self.log.debug("Notifying via gcm/android %r" % recipient)

        if 'registration id' not in recipient:
            self.log.warning("No registration id found.  Bailing.")
            return

        if self.disabled_for(detail_value=recipient['registration id']):
            self.log.debug("Messages stopped for %r, not sending." % nickname)
            return

        self._send_notification(recipient['registration id'], msg)

    def handle_batch(self, recipient, queued_messages):
        raise NotImplementedError()

    def handle_confirmation(self, confirmation):
        confirmation.set_status(self.session, 'valid')
        acceptance_url = self.config['fmn.acceptance_url'].format(
            secret=confirmation.secret)
        rejection_url = self.config['fmn.rejection_url'].format(
            secret=confirmation.secret)

        confirmation_msg = {
            "title": "Fedora Notifications Confirmation"
          , "message": "Hi! Tap this notification to confirm that you would" +
                       " like to receive Fedora related notifications."
          , "secret": confirmation.secret
          }

        self._send_notification(confirmation.detail_value, confirmation_msg)
