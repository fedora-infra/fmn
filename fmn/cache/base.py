# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
import io
import logging
from datetime import datetime
from time import monotonic
from typing import TYPE_CHECKING

from cashews import cache
from cashews.key import get_cache_key_template
from cashews.ttl import ttl_to_seconds
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_engine, make_session_maker
from .util import cache_arg, cache_ttl, lock_ttl

if TYPE_CHECKING:
    from fedora_messaging.message import Message


log = logging.getLogger(__name__)

# Use its own DB connection pool so that async rebuilds don't starve off the consumer's DB pool.
cache_db_session_maker = make_session_maker()


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
        cache_db_session_maker.configure(bind=get_engine())

    async def compute_value(self, db: "AsyncSession"):
        log.debug(f"Building the {self.name} cache")
        before = monotonic()
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        value = await self._compute_value(db=db)
        after = monotonic()
        duration = after - before
        log.debug(f"Built the {self.name} cache in %.2f seconds", duration)
        await cache.set(key=f"duration:{self.name}:{now}", value=int(duration), expire="31d")
        return value

    async def _compute_value(self, db: "AsyncSession"):
        raise NotImplementedError

    async def refresh(self):
        """Rebuild the cache if it is not recent enough."""
        ttl_early = cache_arg("early_ttl", self.name)()
        if not ttl_early:
            return
        ttl_early = ttl_to_seconds(ttl_early)
        refreshed = False
        expire = await cache.get_expire(self._cache_key)
        if expire <= ttl_to_seconds(ttl_early):
            await self.rebuild()
            refreshed = True
        return refreshed

    async def rebuild(self):
        """Rebuild the cache.

        We don't pass the database session here because it is run in the background and we want to
        use our own connection pool.
        """

        async def _rebuild():
            async with cache_db_session_maker.begin() as db:
                ttl = ttl_to_seconds(cache_arg("ttl", self.name)())
                value = await self.compute_value(db=db)
                await cache.set(self._cache_key, value=value, expire=ttl)

        return await cache.locked(key=f"{self.name}:rebuild", ttl=lock_ttl(self.name))(_rebuild)()

    async def invalidate(self, db: "AsyncSession"):
        # This does not really invalidate the cache, instead it rebuilds it in the background
        # because rebuilding is very expensive.
        log.debug(f"Rebuilding the {self.name} cache in the background")
        task = asyncio.create_task(self.rebuild())
        self._background_tasks.add(task)

        def _on_task_done(task):
            self._background_tasks.discard(task)
            exc = task.exception()
            if exc is not None:
                tb = io.StringIO()
                task.print_stack(file=tb)
                log.error(tb.getvalue())

        task.add_done_callback(_on_task_done)

    async def invalidate_on_message(self, message: "Message", db: "AsyncSession"):
        raise NotImplementedError

    async def delete(self):
        log.debug(f"Deleting the {self.name} cache")
        await cache.delete(self._cache_key)
