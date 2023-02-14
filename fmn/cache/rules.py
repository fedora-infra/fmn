import logging
from typing import TYPE_CHECKING

from cashews import cache
from cashews.formatter import get_templates_for_func

from ..database.model import Rule
from .util import cache_early_ttl, cache_ttl

if TYPE_CHECKING:
    from fedora_messaging.message import Message
    from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)


class RulesCache:
    """Cache the rules currently in the database."""

    def __init__(self):
        self.db: "AsyncSession" | None = None

    @cache.early(
        key="rules", prefix="v1", ttl=cache_ttl("rules"), early_ttl=cache_early_ttl("rules")
    )
    @cache.locked(key="rules", prefix="v1", ttl="1h")
    async def get_rules(self):
        if self.db is None:
            raise RuntimeError("You must use set the db attribute first.")
        log.debug("Building the rules cache")
        result = await self.db.execute(Rule.select_related().filter_by(disabled=False))
        log.debug("Built the rules cache")
        return list(result.scalars())

    async def invalidate(self):
        log.debug("Invalidating the rules cache")
        cache_key = list(get_templates_for_func(self.get_rules))[0]
        await cache.delete(cache_key)

    async def invalidate_on_message(self, message: "Message"):
        if (
            message.topic.endswith("fmn.rule.create.v1")
            or message.topic.endswith("fmn.rule.update.v1")
            or message.topic.endswith("fmn.rule.delete.v1")
        ):
            await self.invalidate()
