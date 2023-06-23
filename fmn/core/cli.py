# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
from datetime import datetime, timedelta
from importlib.metadata import entry_points

import click
import click_plugins
from sqlalchemy import delete, func, select

from ..database.main import get_manager
from ..database.model import Generated
from . import config
from .version import __version__


@click_plugins.with_plugins(entry_points(group="fmn.cli"))
@click.group(name="fmn")
@click.option(
    "settings_file",
    "--config",
    "-c",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="The configuration file for FMN.",
)
@click.version_option(version=__version__, prog_name="FMN")
def cli(settings_file: str | None):
    """Fedora Messaging Notifications"""
    if settings_file:
        config.set_settings_file(settings_file)


@cli.group()
def cleanup():
    """Cleanup operations."""


@cleanup.command()
@click.option("--days", type=int, default=31, help="Expire entries older than these many days")
def generated_count(days):
    """Expire old records of generated notification counts."""

    async def _doit():
        limit = datetime.now() - timedelta(days=days)
        db_manager = get_manager()
        async with db_manager.Session.begin() as db:
            result = await db.execute(
                select(func.count(Generated.id)).filter(Generated.when < limit)
            )
            count = result.scalar()
            if count > 0:
                click.echo(f"Expiring {count} entries older than {limit}")
                await db.execute(delete(Generated).filter(Generated.when < limit))
            else:
                click.echo("Nothing to clean up.")

    asyncio.run(_doit())
