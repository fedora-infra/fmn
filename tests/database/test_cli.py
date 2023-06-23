# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from contextlib import nullcontext
from unittest import mock

import pytest
from click import ClickException

from fmn.core.cli import cli
from fmn.core.config import get_settings
from fmn.database import cli as database_cli


@pytest.mark.parametrize("default", (True, False))
@mock.patch("fmn.database.cli.SQLAlchemyModel")
@mock.patch("fmn.database.cli.get_settings")
def test_verify_db_url_not_default(get_settings, SQLAlchemyModel, default):
    default_url = "DEFAULT"
    SQLAlchemyModel.schema.return_value = {"properties": {"url": {"default": default_url}}}
    if default:
        expectation = pytest.raises(ClickException)
        get_settings.return_value.database.sqlalchemy.url = default_url
    else:
        expectation = nullcontext()
        get_settings.return_value.database.sqlalchemy.url = "somethingelse"

    with expectation:
        database_cli.verify_db_url_not_default()


def test_sync(monkeypatch, cli_runner):
    monkeypatch.setattr("fmn.database.cli.verify_db_url_not_default", mock.Mock())
    syncdb = mock.AsyncMock()
    monkeypatch.setattr("fmn.database.cli.syncdb", syncdb)
    result = cli_runner.invoke(cli, ["database", "sync"])

    assert result.exit_code == 0
    syncdb.assert_called_once_with(get_settings().database)


@database_cli.database.command("test")
def _database_test():
    pass


@mock.patch("fmn.database.cli.verify_db_url_not_default")
def test_database(verify_db_url_not_default, cli_runner):
    result = cli_runner.invoke(cli, ["database", "test"])

    assert result.exit_code == 0

    verify_db_url_not_default.assert_called_once_with()
