import json
import logging
import sys
import traceback

import backoff
from aio_pika import Message, connect_robust
from aio_pika.exceptions import AMQPConnectionError

from ..core.amqp import get_url_from_config
from ..rules.notification import Notification

log = logging.getLogger(__name__)


async def backoff_hdlr(details):
    log.warning(f"Publishing message failed. Retrying. {traceback.format_tb(sys.exc_info()[2])}")
    self = details["args"][0]
    await self.connect()


def giveup_hdlr(details):
    log.error(f"Publishing message failed. Giving up. {traceback.format_tb(sys.exc_info()[2])}")


class SendQueue:
    def __init__(self, config: dict):
        self.config = config
        self._url = get_url_from_config(config).update_query(
            connection_name="FMN consumer to sender"
        )
        self._connection = None
        self._channel = None
        self._exchange = None

    async def connect(self):
        self._connection = await connect_robust(self._url)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.get_exchange("amq.direct")

    @backoff.on_exception(
        backoff.expo,
        AMQPConnectionError,
        max_tries=3,
        on_backoff=backoff_hdlr,
        on_giveup=giveup_hdlr,
    )
    async def send(self, notification: Notification):
        body = json.dumps(notification.content)
        await self._exchange.publish(
            Message(body=body.encode("utf-8")),
            routing_key=f"send.{notification.protocol}",
        )

    async def close(self):
        if self._connection:
            await self._connection.close()
