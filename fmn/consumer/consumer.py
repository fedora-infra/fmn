import logging

from fedora_messaging import config

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
        self._cache = get_cache(config.conf["consumer_config"]["cache"])  # noqa
        self._requester = Requester(self._cache)

    def __call__(self, message):
        log.debug(f"Consuming {message!r}")
        try:
            self.handle(message)
        except Exception:
            self.db.rollback()
            raise

    def handle(self, message):
        for rule in Rule.collect(self.db, self._requester):
            notifications = rule.handle(message)
            for n in notifications:
                self.send_queue.send(n)
