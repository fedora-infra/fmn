import logging

from fedora_messaging import config, message

from .cache import cache
from .requester import Requester
from .rule import Rule
from .send_queue import SendQueue

log = logging.getLogger(__name__)


class Consumer:
    def __init__(self):
        # Connect to the database
        self.db = get_database_session(config.conf["consumer_config"]["database_url"])  # noqa
        # Start the connection to RabbitMQ's FMN vhost
        self.send_queue = SendQueue(config.conf["consumer_config"]["send_queue"])
        # Caching and requesting
        cache.configure_from_config(config.conf["consumer_config"]["cache"])
        self._requester = Requester(config.conf["consumer_config"]["services"])

    def __call__(self, message):
        log.debug(f"Consuming {message!r}")
        try:
            self.handle(message)
        except Exception:
            self.db.rollback()
            raise

    def handle(self, message: message.Message):
        self.refresh_cache_if_needed(message)
        if not self.is_tracked(message):
            return
        for rule in Rule.collect(self.db, self._requester):
            notifications = rule.handle(message)
            for n in notifications:
                self.send_queue.send(n)

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
