import asyncio
from datetime import datetime
from unittest import mock

from sqlalchemy import select

from fmn.core import cli, config
from fmn.core.version import __version__
from fmn.database.model import Generated, Rule, TrackingRule, User


@cli.cli.command("test")
def _fmn_test():
    pass


def test_cli_version(cli_runner):
    """Ensure `fmn --version` works."""
    result = cli_runner.invoke(cli.cli, ["--version"])
    assert result.exit_code == 0
    assert result.output == f"FMN, version {__version__}\n"


def test_cli_help(cli_runner):
    """Ensure `fmn --help` works."""
    result = cli_runner.invoke(cli.cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage: fmn" in result.output


@mock.patch.object(config, "_settings_file")
def test_settings(settings_file, cli_runner):
    with mock.patch("fmn.core.config.get_settings") as get_settings:
        result = cli_runner.invoke(cli.cli, [f"--config={__file__}", "test"])
        get_settings.cache_clear.assert_called_once_with()

    assert result.exit_code == 0
    assert config._settings_file == __file__


def test_settings_defaults(cli_runner):
    result = cli_runner.invoke(cli.cli, ["test"])
    assert result.exit_code == 0
    assert config._settings_file == config.DEFAULT_CONFIG_FILE


async def test_cleanup_generated_count(mocker, cli_runner, db_async_session):
    # Delete old entries
    tr = TrackingRule(id=1, name="artifacts-owned", params={"username": "dummy"})
    rule = Rule(id=1, name="dummy", user=User(name="dummy"), tracking_rule=tr, generation_rules=[])
    db_async_session.add(Generated(rule=rule, count=1, when=datetime(2020, 1, 1, 0, 0, 0)))
    await db_async_session.commit()

    mocker.patch("fmn.core.cli.async_session_maker", return_value=db_async_session)
    loop = asyncio.get_event_loop()

    result = await loop.run_in_executor(
        None, cli_runner.invoke, cli.cli, ["cleanup", "generated-count"]
    )

    assert result.exit_code == 0, result.output
    assert result.output.startswith("Expiring 1 entr")
    db_result = await db_async_session.execute(select(Generated))
    assert len(list(db_result.all())) == 0


async def test_cleanup_generated_count_no_old(mocker, cli_runner, db_async_session):
    # Don't delete recent entries
    tr = TrackingRule(id=1, name="artifacts-owned", params={"username": "dummy"})
    rule = Rule(id=1, name="dummy", user=User(name="dummy"), tracking_rule=tr, generation_rules=[])
    db_async_session.add(Generated(rule=rule, count=1))
    await db_async_session.commit()

    mocker.patch("fmn.core.cli.async_session_maker", return_value=db_async_session)
    loop = asyncio.get_event_loop()

    result = await loop.run_in_executor(
        None, cli_runner.invoke, cli.cli, ["cleanup", "generated-count"]
    )

    assert result.exit_code == 0, result.output
    assert result.output == "Nothing to clean up.\n"
    db_result = await db_async_session.execute(select(Generated))
    assert len(list(db_result.all())) == 1
