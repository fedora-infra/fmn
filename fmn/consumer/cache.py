from dogpile.cache import make_region
from fedora_messaging.message import Message

from .rule import Rule


class Cache:
    def __init__(self):
        self.region = make_region(key_mangler=lambda key: f"fmn.c:v1:{key}")
        self.fn_keys = set()

    def build_tracked(self, db, requester):
        # This will be used to quickly know whether we want to process an incoming message or not.
        # It can be called outside of the message-processing loop to refresh the cache.
        # Cases when the cache should be refreshed:
        # - a rule is changed
        # - a user is added or removed to/from a group
        # - an artifact has their owners (users or groups) changed
        # We can have this consumer listen to those events as messages on the bus.
        # If this happens too frequently, we can just refresh after X minutes have passed and tell
        # users that their changes will take X minutes to be active.
        tracked = {
            "packages": set(),
            "containers": set(),
            "modules": set(),
            "flatpaks": set(),
            "usernames": set(),
            "agent_name": set(),
        }
        for rule in Rule.collect(db, requester):
            rule.tracking_rule.prime_cache(tracked)
        return tracked

    def get_tracked(self, db, requester):
        return self.region.get_or_create(
            "tracked", creator=self.build_tracked, creator_args=[db, requester]
        )

    def cache_on_arguments(self, *args, **kwargs):
        return self.region.cache_on_arguments(*args, **kwargs)

    def configure_from_config(self, *args, **kwargs):
        return self.region.configure_from_config(*args, **kwargs)

    def invalidate_tracked(self):
        self.region.delete("tracked")

    def invalidate_on_message(self, message: Message):
        if message.topic.endswith("fmn.rule.updated"):  # XXX: correct topic?
            self.invalidate_tracked()
