from fmn.consumer.backends.base import BaseBackend

import requests


class GCMBackend(BaseBackend):
    def __init__(self, *args, **kwargs):
        super(GCMBackend, self).__init__(*args, **kwargs)
        self.post_url = self.config['fmn.gcm.post_url']
        self.api_key = self.config['fmn.gcm.api_key']

    def handle(self, recipient, msg):
        self.log.debug("Notifying via gcm/android %r" % recipient)

        if 'registration id' not in recipient:
            self.log.warning("No registration id found.  Bailing.")
            return

        headers = {
            'Authorization': 'key=%s' % self.api_key,
            'content-type': 'application/json',
        }
        body = {
            'registration_ids': [recipient['registration id']],
            'data': msg,
        }
        response = requests.post(
            self.post_url,
            data=json.dumps(body),
            headers=headers)
        self.log.debug(" * got %r %r" % (response.status_code, reponse.text))

    def handle_batch(self, recipient, queued_messages):
        raise NotImplementedError()

    def handle_confirmation(self, confirmation):
        raise NotImplementedError()
