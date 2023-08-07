# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

# https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection

from fmn.core.config import get_settings

# Alembic imports this module in a way that it can’t do relative imports from outside the
# fmn/database/migrations directory, therefore it has to use absolute imports.
from fmn.database.main import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
alembic_config = context.config

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = alembic_config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:  # pragma: no cover
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = str(get_settings().database.sqlalchemy.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# https://alembic.sqlalchemy.org/en/latest/cookbook.html#programmatic-api-use-connection-sharing-with-asyncio


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_sync_migrations() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        get_settings().database.sqlalchemy.model_dump(),
        prefix="",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)


def run_migrations_online() -> None:
    connectable = alembic_config.attributes.get("connection", None)

    if connectable is None:
        run_sync_migrations()
    else:
        do_run_migrations(connectable)


if context.is_offline_mode():  # pragma: no cover
    run_migrations_offline()
else:
    run_migrations_online()
