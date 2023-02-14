import logging
from dataclasses import dataclass, field
from time import monotonic
from typing import TYPE_CHECKING

from cashews import cache
from cashews.formatter import get_templates_for_func

if TYPE_CHECKING:
    from fedora_messaging.message import Message

    from ..rules.requester import Requester
    from .rules import RulesCache

log = logging.getLogger(__name__)


@dataclass
class Tracked:
    packages: set = field(default_factory=set)
    containers: set = field(default_factory=set)
    modules: set = field(default_factory=set)
    flatpaks: set = field(default_factory=set)
    usernames: set = field(default_factory=set)
    agent_name: set = field(default_factory=set)


class TrackedCache:
    """Used to quickly know whether we want to process an incoming message.

    It can be called outside of the message-processing loop to refresh the cache.

    Cases when the cache should be refreshed:
    - a rule is changed
    - a user is added or removed to/from a group
    - an artifact has their owners (users or groups) changed

    The Consumer listens to those events as messages on the bus.

    If this happens too frequently, we can just refresh after X minutes have passed and tell
    users that their changes will take X minutes to be active.
    """

    def __init__(self, rules_cache: "RulesCache"):
        self._rules_cache = rules_cache

    @cache.locked(key="tracked", prefix="v1", ttl="1h")
    async def build(self, requester: "Requester"):
        log.debug("Building the tracked cache")
        before = monotonic()
        tracked = Tracked()
        for rule in await self._rules_cache.get_rules():
            await rule.tracking_rule.prime_cache(tracked, requester)
        after = monotonic()
        duration = after - before
        log.debug(f"Built the tracked cache in {duration:.2f} seconds")
        return tracked

    @cache.early(key="tracked", prefix="v1", ttl="1d", early_ttl="22h")
    async def get_tracked(self, requester: "Requester"):
        return await self.build(requester=requester)

    async def invalidate(self):
        log.debug("Invalidating the tracked cache")
        cache_key = list(get_templates_for_func(self.get_tracked))[0]
        await cache.delete(cache_key)

    async def invalidate_on_message(self, message: "Message"):
        if (
            message.topic.endswith("fmn.rule.create.v1")
            or message.topic.endswith("fmn.rule.update.v1")
            or message.topic.endswith("fmn.rule.delete.v1")
        ):
            await self.invalidate()
