import asyncio
from pprint import pprint

import click

from fmn.cache import configure_cache
from fmn.cache.tracked import TrackedCache
from fmn.core.config import get_settings
from fmn.database import async_session_maker, init_sync_model

from .requester import Requester


@click.group("cache")
def cache_cmd():
    """Work with the cache in FMN."""


@cache_cmd.command("get-tracked")
def get_tracked():
    """Show the current tracked value."""
    configure_cache()
    init_sync_model()
    db = async_session_maker()
    requester = Requester(get_settings().services)
    tracked_cache = TrackedCache()
    result = asyncio.run(tracked_cache.get_tracked(db, requester))
    pprint(result)


@cache_cmd.command("delete-tracked")
def delete_tracked():
    """Invalidate the current tracked value."""
    configure_cache()
    tracked_cache = TrackedCache()
    asyncio.run(tracked_cache.invalidate())
    print("Tracked cache invalidated.")
