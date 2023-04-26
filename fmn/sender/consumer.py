# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import json
import logging

from aio_pika import connect_robust

from ..core.amqp import get_url_from_config

log = logging.getLogger(__name__)


CLOSING = object()


class Consumer:
    def __init__(self, config, handler):
        self._destination = config["queue"]
        self._url = get_url_from_config(config).update_query(
            connection_name=f"FMN sender on {self._destination}"
        )
        self._handler = handler
        self._connection = None
        self._channel = None
        self._queue = None
        self._queue_iter = None

    async def connect(self):
        self._connection = await connect_robust(self._url)
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(
            self._destination, durable=True, auto_delete=False, exclusive=False
        )
        await self._queue.bind("amq.direct", f"send.{self._destination}")

    async def start(self):
        log.info("Starting consuming messages")
        async with self._queue.iterator() as self._queue_iter:
            async for message in self._queue_iter:
                if message == CLOSING:
                    log.debug("Got close message, breaking out of the loop")
                    break
                async with message.process():
                    await self._handler.handle(json.loads(message.body))

        await self._queue_iter.close()
        log.debug("Finished consuming messages")

    async def stop(self):
        log.info("Stopping messages consumption")
        if self._queue_iter:
            await self._queue_iter.on_message(CLOSING)
            # Close the queue now or closing the connection just below will cancel the iterator
            # and raise an exception in start()
            await self._queue_iter.close()
        if self._connection:
            await self._connection.close()
        await self._handler.stop()
