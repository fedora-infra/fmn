import logging

from fedora_messaging import message
from fedora_messaging.config import conf as fm_config

from fmn.core import config
from fmn.database import init_sync_model, sync_session_maker

from .cache import cache
from .requester import Requester
from .rule import Rule
from .send_queue import SendQueue

log = logging.getLogger(__name__)


class Consumer:
    def __init__(self):
        # Load the general config
        if fm_config.get("settings_file"):
            config.set_settings_file(fm_config["settings_file"])
        # Connect to the database
        init_sync_model()
        self.db = sync_session_maker()
        # Start the connection to RabbitMQ's FMN vhost
        self.send_queue = SendQueue(fm_config["consumer_config"]["send_queue"])
        self.send_queue.connect()
        # Caching and requesting
        cache.configure(**config.get_settings().dict()["cache"])
        self._requester = Requester(config.get_settings().dict()["services"])

    def __call__(self, message):
        log.debug(f"Consuming message {message.id}")
        try:
            self.handle(message)
        except Exception:
            self.db.rollback()
            raise

    def handle(self, message: message.Message):
        self.refresh_cache_if_needed(message)
        if not self.is_tracked(message):
            log.debug(f"Message {message.id} is not tracked")
            return
        for rule in Rule.collect(self.db, self._requester):
            for notification in rule.handle(message):
                log.debug(
                    f"Generating notification for message {message.id} via {notification.protocol}"
                )
                self.send_queue.send(notification)

    def is_tracked(self, message: message.Message):
        # This is cache-based and should save us running all the messages through all the rules. The
        # tracked messages will still run though all the rules though, so this could be improved I
        # suppose, maybe by changing the cache datastructure to point each entry in the cache to the
        # rules that produced it.
        tracked = cache.get_tracked(self.db, self._requester)
        for msg_attr in ("packages", "containers", "modules", "flatpaks", "usernames"):
            if not set(getattr(message, msg_attr)).isdisjoint(tracked[msg_attr]):
                return True
        if message.agent_name in tracked["agent_name"]:
            return True
        return False

    def refresh_cache_if_needed(self, message: message.Message):
        cache.invalidate_on_message(message)
        self._requester.invalidate_on_message(message)
