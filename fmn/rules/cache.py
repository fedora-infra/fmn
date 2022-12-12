import logging
from typing import TYPE_CHECKING

from dogpile.cache import make_region

from fmn.core import config
from fmn.database.model import Rule

if TYPE_CHECKING:
    from fedora_messaging.message import Message
    from sqlalchemy.orm import Session

    from .requester import Requester

log = logging.getLogger(__name__)


class Cache:
    def __init__(self):
        self.region = make_region(key_mangler=lambda key: f"fmn.c:v1:{key}")

    def build_tracked(self, db: "Session", requester: "Requester"):
        # This will be used to quickly know whether we want to process an incoming message or not.
        # It can be called outside of the message-processing loop to refresh the cache.
        # Cases when the cache should be refreshed:
        # - a rule is changed
        # - a user is added or removed to/from a group
        # - an artifact has their owners (users or groups) changed
        # We can have this consumer listen to those events as messages on the bus.
        # If this happens too frequently, we can just refresh after X minutes have passed and tell
        # users that their changes will take X minutes to be active.

        log.debug("Building the tracked cache")
        tracked = {
            "packages": set(),
            "containers": set(),
            "modules": set(),
            "flatpaks": set(),
            "usernames": set(),
            "agent_name": set(),
        }
        rules = db.execute(Rule.select_related().filter_by(disabled=False)).scalars()
        for rule in rules:
            rule.tracking_rule.prime_cache(tracked, requester)
        log.debug("Built the tracked cache")
        return tracked

    def get_tracked(self, db: "Session", requester: "Requester"):
        return self.region.get_or_create(
            "tracked",
            creator=self.build_tracked,
            creator_args=(tuple(), {"db": db, "requester": requester}),
        )

    def cache_on_arguments(self, *args, **kwargs):
        return self.region.cache_on_arguments(*args, **kwargs)

    def configure(self, **kwargs):
        conf = config.get_settings().dict()["cache"]
        conf.update(kwargs)
        return self.region.configure(**conf)

    def invalidate_tracked(self):
        log.debug("Invalidating the tracked cache")
        self.region.delete("tracked")

    def invalidate_on_message(self, message: "Message", db: "Session", requester: "Requester"):
        if (
            message.topic.endswith("fmn.rule.create.v1")
            or message.topic.endswith("fmn.rule.update.v1")
            or message.topic.endswith("fmn.rule.delete.v1")
        ):
            self.invalidate_tracked()
            self.build_tracked(db, requester)


cache = Cache()
