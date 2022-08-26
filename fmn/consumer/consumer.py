import logging

from fedora_messaging import config

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

    def handle(self, message):
        for rule in Rule.collect(self.db, self._requester):
            notifications = rule.handle(message)
            for n in notifications:
                self.send_queue.send(n)
