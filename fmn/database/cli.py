# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import click

from ..core.config import SQLAlchemyModel, get_settings
from .migrations.main import alembic_migration
from .setup import setup_db_schema


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
def setup():
    """Set up FMN in the configured database."""
    setup_db_schema()


@database.group()
def migration():
    """Manage database migrations for FMN."""
    pass


@migration.command("create")
@click.option(
    "--autogenerate/--no-autogenerate",
    default=False,
    help="Autogenerate migration script skeleton (needs to be reviewed/edited).",
)
@click.argument("comment", nargs=-1, required=True)
def migration_create(autogenerate, comment):
    """Create a new database schema migration."""
    alembic_migration.create(comment=" ".join(comment), autogenerate=autogenerate)


@migration.command("db-version")
def migration_db_version():
    """Show the current version of the database schema."""
    alembic_migration.db_version()


@migration.command("upgrade")
@click.argument("version", default="head")
def migration_upgrade(version):
    """Upgrade the database schema."""
    alembic_migration.upgrade(version)


@migration.command("downgrade")
@click.argument("version", default="-1")
def migration_downgrade(version):
    """Downgrade the database schema."""
    alembic_migration.downgrade(version)
