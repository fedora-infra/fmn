# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import sys
from pathlib import Path

import alembic.command
import alembic.config
from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from ..core.config import get_settings

# Import the DB model here so its classes are considered by metadata.create_all() below.
from . import model  # noqa: F401
from .main import get_sync_engine, metadata

HERE = Path(__file__).parent


def setup_db_schema(engine_or_session: Engine | Session | None = None) -> None:
    if isinstance(engine_or_session, Session):
        engine = engine_or_session.get_bind()
    else:
        engine = engine_or_session or get_sync_engine()

    inspection_result = inspect(engine)

    present_tables = sorted(n for n in metadata.tables if inspection_result.has_table(n))

    if present_tables:
        print(f"Tables already present: {', '.join(present_tables)}", file=sys.stderr)
        print("Refusing to change database schema.", file=sys.stderr)
        sys.exit(1)

    with engine.begin():
        print("Creating database schema")
        metadata.create_all(bind=engine)

        print("Setting up database migrations")
        cfg = alembic.config.Config()
        cfg.set_main_option("script_location", str(HERE / "migrations"))
        cfg.set_main_option("sqlalchemy.url", get_settings().database.sqlalchemy.url)

        alembic.command.stamp(cfg, "head")
