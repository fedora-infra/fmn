import json
import logging
import ssl

from aio_pika import connect_robust
from aio_pika.abc import SSLOptions

_log = logging.getLogger(__name__)


CLOSING = object()


class Consumer:
    def __init__(self, config, handler):
        self._url = config["amqp_url"]
        self._destination = config["queue"]
        self._handler = handler
        if "tls" in config:
            self._ssl_options = SSLOptions(
                cafile=config["tls"]["ca_cert"],
                certfile=config["tls"]["certfile"],
                keyfile=config["tls"]["keyfile"],
                no_verify_ssl=ssl.CERT_REQUIRED,
            )
        else:
            self._ssl_options = None
        self._connection = None
        self._channel = None
        self._queue = None
        self._queue_iter = None

    async def connect(self):
        self._connection = await connect_robust(
            self._url, ssl_options=self._ssl_options, client_properties={"connection_name": "FMN"}
        )
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(
            self._destination, durable=True, auto_delete=False, exclusive=False
        )
        await self._queue.bind("amq.direct", f"send.{self._destination}")

    async def start(self):
        _log.info("Starting consuming messages")
        async with self._queue.iterator() as self._queue_iter:
            async for message in self._queue_iter:
                if message == CLOSING:
                    break
                async with message.process():
                    await self._handler.handle(json.loads(message.body))

    async def stop(self):
        if self._queue_iter:
            await self._queue_iter.on_message(CLOSING)
            await self._queue_iter.close()
        if self._connection:
            await self._connection.close()
        await self._handler.stop()
