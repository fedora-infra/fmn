# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from contextlib import nullcontext
from unittest import mock

import pytest

from fmn.core.config import get_settings
from fmn.database import setup


@pytest.mark.parametrize("db_empty", (True, False))
@mock.patch("fmn.database.setup.alembic.command.stamp")
@mock.patch("fmn.database.setup.alembic.config.Config")
@mock.patch("fmn.database.setup.metadata")
@mock.patch("fmn.database.setup.inspect")
@mock.patch("fmn.database.setup.get_engine")
def test_setup_db_schema(get_engine, inspect, metadata, Config, stamp, db_empty):
    engine = mock.MagicMock()
    get_engine.return_value = engine

    inspection_result = mock.MagicMock()
    inspection_result.has_table.return_value = not db_empty
    inspect.return_value = inspection_result

    metadata.tables = {"table1": object(), "table2": object()}

    Config.return_value = cfg = mock.Mock()

    if db_empty:
        expectation = nullcontext()
    else:
        expectation = pytest.raises(SystemExit)

    with expectation:
        setup.setup_db_schema()

    if db_empty:
        get_engine.assert_called_once_with(sync=True)
        engine.begin.assert_called_once_with()
        metadata.create_all.assert_called_once_with(bind=engine)
        cfg.set_main_option.assert_any_call("script_location", str(setup.HERE / "migrations"))
        cfg.set_main_option.assert_any_call(
            "sqlalchemy.url", get_settings().database.sqlalchemy.url
        )
    else:
        engine.begin.assert_not_called()
        metadata.create_all.assert_not_called()
        Config.assert_not_called()
