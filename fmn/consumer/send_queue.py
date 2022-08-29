import json

import pika

from .notification import Notification


class SendQueue:
    def __init__(self, config):
        self.config = config
        self._connection = None
        self._channel = None

    def connect(self):
        self._connection = pika.BlockingConnection(self.config["url"])
        self._channel = self._connection.channel()

    def send(self, notification: Notification):
        body = json.dumps(notification.content)
        self.channel.basic_publish(
            exchange="amq.direct", routing_key=f"send.{notification.destination}", body=body
        )

    def close(self):
        self._connection.close()
