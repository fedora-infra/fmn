import asyncio
import logging
from time import monotonic
from typing import TYPE_CHECKING

from cashews import cache
from cashews.formatter import get_templates_for_func

if TYPE_CHECKING:
    from fedora_messaging.message import Message

log = logging.getLogger(__name__)


class CachedValue:
    """Manage a cached value."""

    name = None

    async def get_value(self, *args, **kwargs):
        # This method must be decorated with the cache decorator.
        return await self.compute_value(*args, **kwargs)

    async def compute_value(self, *args, **kwargs):
        log.debug(f"Building the {self.name} cache")
        before = monotonic()
        value = await self._compute_value(*args, **kwargs)
        after = monotonic()
        duration = after - before
        log.debug(f"Built the {self.name} cache in %.2f seconds", duration)
        return value

    async def _compute_value(self, *args, **kwargs):
        raise NotImplementedError

    async def invalidate(self):
        log.debug(f"Invalidating the {self.name} cache")
        cache_keys = get_templates_for_func(self.get_value)
        await asyncio.gather(*(cache.delete(key) for key in cache_keys))

    async def invalidate_on_message(self, message: "Message"):
        raise NotImplementedError
