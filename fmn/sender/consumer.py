import logging

import pika

_log = logging.getLogger(__name__)


class Consumer:
    def __init__(self, url, destination, handler):
        self._url = url
        self._destination = destination
        self._handler = handler
        self._connection = None
        self._channel = None

    def connect(self):
        self._connection = pika.BlockingConnection(pika.connection.URLParameters(self._url))
        self._channel = self._connection.channel()
        self._channel.queue_declare(
            self._destination, durable=True, auto_delete=False, exclusive=False
        )
        self._channel.queue_bind(self._destination, "amq.direct", f"send.{self._destination}")

    def start(self):
        self._channel.basic_consume(self._destination, self._handler.on_message)
        _log.info("Started consuming")
        self._channel.start_consuming()

    def stop(self):
        if self._channel:
            self._channel.stop_consuming()
        if self._connection:
            self._connection.close()
        self._handler.stop()
