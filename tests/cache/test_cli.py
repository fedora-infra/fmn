# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
from unittest import mock

import pytest
from cashews import cache

from fmn.cache import configure_cache
from fmn.core.cli import cli
from fmn.core.config import get_settings


@pytest.fixture
def mocked_session_maker(mocker, db_async_session):
    db_manager = mock.Mock()
    transaction_manager = mock.AsyncMock()
    mocker.patch("fmn.cache.cli.get_manager", return_value=db_manager)
    db_manager.Session.begin.return_value = transaction_manager
    transaction_manager.__aenter__.return_value = db_async_session
    return transaction_manager


@pytest.fixture
def persistent_cache(mocker, tmpdir, cli_runner):
    cache_url = f"disk://?directory={tmpdir}/cache&timeout=1&shards=0"
    mocker.patch.object(get_settings().cache, "url", cache_url)
    configure_cache()
    cli_runner.env = {"CACHE__URL": get_settings().cache.url}


def test_get_tracked(mocker, cli_runner, mocked_fasjson_proxy, mocked_tracked_cache, db_manager):
    configure_cache = mocker.patch("fmn.cache.cli.configure_cache")
    mocker.patch("fmn.cache.cli.get_manager", return_value=db_manager)
    mocked_tracked_cache.get_value.return_value = {"foo": "bar"}

    result = cli_runner.invoke(cli, ["cache", "get-tracked"])

    assert result.exit_code == 0, result.output
    configure_cache.assert_called_once_with(db_manager=db_manager)
    mocked_tracked_cache.get_value.assert_called_once()
    assert result.output == "{'foo': 'bar'}\n"


def test_delete_tracked(mocker, cli_runner):
    configure_cache = mocker.patch("fmn.cache.cli.configure_cache")
    cache = mocker.patch("fmn.cache.base.cache")
    cache.delete = mock.AsyncMock()

    result = cli_runner.invoke(cli, ["cache", "delete-tracked"])

    assert result.exit_code == 0, result.output
    configure_cache.assert_called_once_with()
    cache.delete.assert_called_once_with("v1:tracked")


@pytest.mark.cashews_cache(enabled=True)
def test_refresh_new(mocker, cli_runner, mocked_session_maker):
    result = cli_runner.invoke(cli, ["cache", "refresh"])
    assert result.exit_code == 0
    assert all("Refreshed the" in line for line in result.output.splitlines())


@pytest.mark.cashews_cache(enabled=True)
def test_refresh_recent(mocker, cli_runner, mocked_session_maker, persistent_cache):
    async def _set_cache():
        # Set the expiration higher than early_ttl
        await cache.set("v1:rules", value="dummy", expire=86400)
        await cache.set("v1:tracked", value="dummy", expire=86400)

    asyncio.run(_set_cache())
    result = cli_runner.invoke(cli, ["cache", "refresh"])
    assert result.exit_code == 0
    assert all("is recent enough." in line for line in result.output.splitlines())


@pytest.mark.cashews_cache(enabled=True)
def test_refresh_old(mocker, cli_runner, mocked_session_maker, persistent_cache):
    async def _set_cache():
        # Set the expiration lower than early_ttl
        await cache.set("v1:rules", value="dummy", expire=42)
        await cache.set("v1:tracked", value="dummy", expire=42)

    asyncio.run(_set_cache())

    result = cli_runner.invoke(cli, ["cache", "refresh"])
    assert result.exit_code == 0
    assert all("Refreshed the" in line for line in result.output.splitlines())


@pytest.mark.cashews_cache(enabled=True)
def test_refresh_no_early_ttl(mocker, cli_runner, mocked_session_maker):
    cache_arg = mocker.patch("fmn.cache.base.cache_arg", return_value=lambda: None)
    result = cli_runner.invoke(cli, ["cache", "refresh"])
    assert cache_arg.call_count == 2
    cache_arg.assert_has_calls(
        [
            mock.call("early_ttl", "rules"),
            mock.call("early_ttl", "tracked"),
        ]
    )
    assert result.exit_code == 0
    assert all("has no early refresh configured." in line for line in result.output.splitlines())


@pytest.mark.cashews_cache(enabled=True)
def test_delete_locks(mocker, cli_runner):
    async def _set_cache():
        await cache.set("locked:foo", value="dummy")
        await cache.set("locked:bar", value="dummy")

    mocker.patch("fmn.cache.cli.configure_cache")
    asyncio.run(_set_cache())
    result = cli_runner.invoke(cli, ["cache", "delete-locks"])

    assert result.exit_code == 0, result.output
    assert result.output == "Deleted lock for foo\nDeleted lock for bar\nCache locks deleted.\n"


@pytest.mark.cashews_cache(enabled=True)
def test_get_build_durations(mocker, cli_runner):
    async def _set_cache():
        await cache.set("duration:foo:2022-01-01T01:01:01", value=42.42424242)
        await cache.set("duration:bar:2023-02-01T01:01:01", value=12.345678)

    mocker.patch("fmn.cache.cli.configure_cache")
    asyncio.run(_set_cache())
    result = cli_runner.invoke(cli, ["cache", "get-build-durations"])

    assert result.exit_code == 0, result.output
    expected_msg = (
        "Built bar on 2023-02-01T01:01:01 in 12.35s\n"
        "Built foo on 2022-01-01T01:01:01 in 42.42s\n"
    )
    assert result.output == expected_msg
