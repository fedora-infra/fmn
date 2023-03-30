# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from contextlib import nullcontext
from unittest import mock

import pytest
from click import ClickException

from fmn.core.cli import cli
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


@database_cli.database.command("test")
def _database_test():
    pass


@mock.patch("fmn.database.cli.verify_db_url_not_default")
def test_database(verify_db_url_not_default, cli_runner):
    result = cli_runner.invoke(cli, ["database", "test"])

    assert result.exit_code == 0

    verify_db_url_not_default.assert_called_once_with()


@mock.patch("fmn.database.cli.setup_db_schema")
@mock.patch("fmn.database.cli.verify_db_url_not_default", new=mock.Mock())
def test_setup(setup_db_schema, cli_runner):
    result = cli_runner.invoke(cli, ["database", "setup"])

    assert result.exit_code == 0

    setup_db_schema.assert_called_once_with()


@mock.patch("fmn.database.cli.alembic_migration")
@mock.patch("fmn.database.cli.verify_db_url_not_default", new=mock.Mock())
class TestMigrationCLI:
    @pytest.mark.parametrize("testcase", ("normal", "autogenerate", "missing-comment"))
    def test_migration_create(self, alembic_migration, testcase, cli_runner):
        comment = "A comment"
        args = ["database", "migration", "create"]
        if testcase == "autogenerate":
            args.append("--autogenerate")
        if testcase != "missing-comment":
            args.extend(comment.split())

        result = cli_runner.invoke(cli, args)

        if testcase == "missing-comment":
            assert result.exit_code != 0
        else:
            assert result.exit_code == 0
            alembic_migration.create.assert_called_once_with(
                comment=comment, autogenerate=(testcase == "autogenerate")
            )

    def test_migration_db_version(self, alembic_migration, cli_runner):
        result = cli_runner.invoke(cli, ["database", "migration", "db-version"])
        assert result.exit_code == 0
        alembic_migration.db_version.assert_called_once_with()

    @pytest.mark.parametrize("subcommand", ("upgrade", "downgrade"))
    def test_migration_upgrade_downgrade(self, alembic_migration, subcommand, cli_runner):
        result = cli_runner.invoke(cli, ["database", "migration", subcommand, "BOO"])
        assert result.exit_code == 0
        getattr(alembic_migration, subcommand).assert_called_once_with("BOO")
