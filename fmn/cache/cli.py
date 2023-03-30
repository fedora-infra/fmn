# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
from pprint import pformat
from time import monotonic

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
        tracked_cache = TrackedCache(requester=requester, rules_cache=rules_cache)
        async with async_session_maker.begin() as db:
            return await tracked_cache.get_value(db=db)

    result = asyncio.run(_get_tracked())
    click.echo(pformat(result))


@cache_cmd.command("delete-tracked")
def delete_tracked():
    """Invalidate the current tracked value."""
    configure_cache()
    requester = Requester(get_settings().services)
    rules_cache = RulesCache()
    tracked_cache = TrackedCache(requester=requester, rules_cache=rules_cache)
    asyncio.run(tracked_cache.invalidate())
    click.echo("Tracked cache invalidated.")


@cache_cmd.command("refresh")
def refresh():
    """Refresh the cached values if they have reached their early_ttl."""

    async def _doit():
        configure_cache()
        await init_async_model()
        requester = Requester(get_settings().services)
        rules_cache = RulesCache()
        tracked_cache = TrackedCache(requester=requester, rules_cache=rules_cache)
        async with async_session_maker.begin() as db:
            for cache_value in (rules_cache, tracked_cache):
                before = monotonic()
                refreshed = await cache_value.refresh(db=db)
                after = monotonic()
                duration = after - before
                if refreshed is None:
                    click.echo(f"The {cache_value.name} cache has no early refresh configured.")
                elif refreshed:
                    click.echo(f"Refreshed the {cache_value.name} cache in {duration:.0f}s.")
                else:
                    click.echo(f"The {cache_value.name} cache is recent enough.")

    asyncio.run(_doit())
