# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
import logging
from time import monotonic
from typing import TYPE_CHECKING

from cashews import cache
from cashews.key import get_cache_key_template
from cashews.ttl import ttl_to_seconds

from .util import cache_arg, cache_ttl, lock_ttl

if TYPE_CHECKING:
    from fedora_messaging.message import Message
    from sqlalchemy.ext.asyncio import AsyncSession


log = logging.getLogger(__name__)


class CachedValue:
    """Manage a cached value."""

    name = None
    cache_version = "v1"
    _background_tasks = set()

    def __init__(self):
        # Define the function here instead of wrapping it in a regular async function because the
        # cashew decorators are designed to wrap once on init, and do a lot of pre-processing.
        self.get_value = cache.locked(key=self.name, ttl=lock_ttl(self.name))(
            # Don't use the lock=True option of the decorator because it does not allow to set
            # the ttl for the lock itself.
            cache(key=self.name, prefix=self.cache_version, ttl=cache_ttl(self.name))(
                self.compute_value
            )
        )
        self._cache_key = get_cache_key_template(
            self.get_value, key=self.name, prefix=self.cache_version
        )

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

    async def refresh(self, *args, **kwargs):
        async def _refresh():
            ttl_early = cache_arg("early_ttl", self.name)()
            if not ttl_early:
                return
            ttl_early = ttl_to_seconds(ttl_early)
            refreshed = False
            expire = await cache.get_expire(self._cache_key)
            if expire <= ttl_to_seconds(ttl_early):
                ttl = ttl_to_seconds(cache_arg("ttl", self.name)())
                value = await self.compute_value(*args, **kwargs)
                await cache.set(self._cache_key, value=value, expire=ttl)
                refreshed = True
            return refreshed

        return await cache.locked(key=self.name, ttl=lock_ttl(self.name))(_refresh)()

    async def invalidate(self, *args, **kwargs):
        # This does not really invalidate the cache, instead it rebuilds it in the background
        # because it's very expensive.
        log.debug(f"Rebuilding the {self.name} cache in the background")
        task = asyncio.create_task(self.refresh(*args, **kwargs))
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

    async def invalidate_on_message(self, message: "Message", db: "AsyncSession"):
        raise NotImplementedError

    async def delete(self):
        log.debug(f"Deleting the {self.name} cache")
        await cache.delete(self._cache_key)
