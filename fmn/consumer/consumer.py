import asyncio
import logging
from concurrent.futures import wait

from aio_pika.exceptions import AMQPConnectionError
from fedora_messaging import message
from fedora_messaging.config import conf as fm_config
from fedora_messaging.exceptions import Nack

from ..cache import configure_cache
from ..cache.rules import RulesCache
from ..cache.tracked import TrackedCache
from ..core import config
from ..database import async_session_maker, init_async_model
from ..database.model import Generated
from ..rules.requester import Requester
from .send_queue import SendQueue

log = logging.getLogger(__name__)


class Consumer:
    def __init__(self):
        # Load the general config
        if fm_config["consumer_config"].get("settings_file"):
            config.set_settings_file(fm_config["consumer_config"]["settings_file"])
        self._rules_cache = RulesCache()
        self._requester = Requester(config.get_settings().services)
        self._tracked_cache = TrackedCache(requester=self._requester, rules_cache=self._rules_cache)
        self.send_queue = SendQueue(fm_config["consumer_config"]["send_queue"])
        self.loop = asyncio.get_event_loop()
        self._ready = self.loop.create_task(self.setup())
        if not self.loop.is_running():
            self.loop.run_until_complete(self._ready)

    async def setup(self):
        # Connect to the database
        await init_async_model()
        self.db = async_session_maker()
        self._rules_cache.db = self.db
        # Start the connection to RabbitMQ's FMN vhost
        await self.send_queue.connect()
        # Caching and requesting
        configure_cache()

    def __call__(self, message: message.Message):
        log.debug("Consuming message %s", message.id)
        coro = self.handle_or_rollback(message)
        if self.loop.is_running():
            # We're running with Fedora Messaging >= 3.3.0, that uses asyncio
            # for its reactor.
            wait([asyncio.run_coroutine_threadsafe(coro, self.loop)])
        else:
            self.loop.run_until_complete(coro)

    async def handle_or_rollback(self, message: message.Message):
        await self._ready
        try:
            await self.handle(message)
        except Exception:
            await self.db.rollback()
            raise
        else:
            await self.db.commit()

    async def handle(self, message: message.Message):
        await self.refresh_cache_if_needed(message)
        if not await self.is_tracked(message):
            log.debug("Message %s is not tracked", message.id)
            return
        if message.deprecated:
            # The sender will also send the message with the new schema, don't duplicate
            # notifications.
            return
        for rule in await self._rules_cache.get_rules():
            async for notification in rule.handle(message, self._requester):
                await self._send(notification, message)
                # Record that the rule generated a notification
                self.db.add(Generated(rule=rule, count=1))
                await self.db.commit()

    async def _send(self, notification, from_msg):
        log.debug(
            "Generating notification for message %s via %s", from_msg.id, notification.protocol
        )
        try:
            await self.send_queue.send(notification)
        except AMQPConnectionError as e:
            log.error(
                "Could not send notification for %s via %s: %s",
                from_msg.id,
                notification.protocol,
                e,
            )
            raise Nack()

    async def is_tracked(self, message: message.Message):
        # This is cache-based and should save us running all the messages through all the rules. The
        # tracked messages will still run though all the rules though, so this could be improved I
        # suppose, maybe by changing the cache datastructure to point each entry in the cache to the
        # rules that produced it.
        tracked = await self._tracked_cache.get_tracked()
        for msg_attr in ("packages", "containers", "modules", "flatpaks", "usernames"):
            if not set(getattr(message, msg_attr)).isdisjoint(getattr(tracked, msg_attr)):
                log.debug("Message %s is tracked by %s", message.id, msg_attr)
                return True
        if message.agent_name in tracked.agent_name:
            log.debug("Message %s is tracked by agent_name", message.id)
            return True
        return False

    async def refresh_cache_if_needed(self, message: message.Message):
        await self._rules_cache.invalidate_on_message(message)
        await self._tracked_cache.invalidate_on_message(message)
        await self._requester.invalidate_on_message(message)
