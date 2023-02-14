import asyncio
from pprint import pprint

import click

from ..core.config import get_settings
from ..database import async_session_maker, init_async_model
from ..rules.requester import Requester
from . import configure_cache
from .rules import RulesCache
from .tracked import TrackedCache


@click.group("cache")
def cache_cmd():
    """Work with the cache in FMN."""


@cache_cmd.command("get-tracked")
def get_tracked():
    """Show the current tracked value."""

    async def _get_tracked():
        configure_cache()
        await init_async_model()
        requester = Requester(get_settings().services)
        rules_cache = RulesCache()
        tracked_cache = TrackedCache(rules_cache=rules_cache)
        async with async_session_maker() as db:
            rules_cache.db = db
            return await tracked_cache.get_tracked(requester)

    result = asyncio.run(_get_tracked())
    pprint(result)


@cache_cmd.command("delete-tracked")
def delete_tracked():
    """Invalidate the current tracked value."""
    configure_cache()
    rules_cache = RulesCache()
    tracked_cache = TrackedCache(rules_cache=rules_cache)
    asyncio.run(tracked_cache.invalidate())
    print("Tracked cache invalidated.")
