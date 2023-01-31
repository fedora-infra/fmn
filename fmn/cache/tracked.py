import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from cashews import cache
from cashews.formatter import get_templates_for_func

from fmn.database.model import Rule

if TYPE_CHECKING:
    from fedora_messaging.message import Message
    from sqlalchemy.ext.asyncio import AsyncSession

    from ..rules.requester import Requester

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

    @cache.locked(key="tracked", prefix="v1", ttl="1h")
    async def build(self, db: "AsyncSession", requester: "Requester"):
        log.debug("Building the tracked cache")
        tracked = Tracked()
        db_result = await db.execute(Rule.select_related().filter_by(disabled=False))
        for rule in db_result.scalars():
            await rule.tracking_rule.prime_cache(tracked, requester)
        log.debug("Built the tracked cache")
        return tracked

    @cache.early(key="tracked", prefix="v1", ttl="1d", early_ttl="22h")
    async def get_tracked(self, db: "AsyncSession", requester: "Requester"):
        return await self.build(db=db, requester=requester)

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
