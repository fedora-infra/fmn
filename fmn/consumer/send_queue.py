import json

import pika

from fmn.rules.notification import Notification


class SendQueue:
    def __init__(self, config):
        self.config = config
        self._connection = None
        self._channel = None

    def connect(self):
        parameters = pika.URLParameters(self.config["url"])
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

    def send(self, notification: Notification):
        body = json.dumps(notification.content)
        self._channel.basic_publish(
            exchange="amq.direct", routing_key=f"send.{notification.protocol}", body=body
        )

    def close(self):
        self._connection.close()
