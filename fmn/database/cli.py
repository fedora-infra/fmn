# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio

import click
from sqlalchemy_helpers.fastapi import syncdb

from ..core.config import SQLAlchemyModel, get_settings


def verify_db_url_not_default():
    """Verify the DB URL is set to a valid value."""
    if (
        get_settings().database.sqlalchemy.url
        == SQLAlchemyModel.schema()["properties"]["url"]["default"]
    ):
        raise click.ClickException("The database URL must be set to a non-default value.")


@click.group()
def database():
    """Work with the database used by FMN."""
    verify_db_url_not_default()


@database.command()
def sync():
    """Set up FMN in the configured database."""
    asyncio.run(syncdb(get_settings().database))
