# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
from unittest import mock

import pytest
from cashews import cache

from fmn.cache import configure_cache
from fmn.cache.tracked import TrackedCache
from fmn.core.cli import cli
from fmn.core.config import get_settings


@pytest.fixture
def mocked_session_maker(mocker, db_async_session):
    transaction_manager = mock.AsyncMock()
    sessionmaker = mocker.patch("fmn.cache.cli.async_session_maker")
    sessionmaker.begin.return_value = transaction_manager
    transaction_manager.__aenter__.return_value = db_async_session
    return transaction_manager


@pytest.fixture
def persistent_cache(mocker, tmpdir, cli_runner):
    cache_url = f"disk://?directory={tmpdir}/cache&timeout=1&shards=0"
    mocker.patch.object(get_settings().cache, "url", cache_url)
    configure_cache()
    cli_runner.env = {"CACHE__URL": get_settings().cache.url}


def test_get_tracked(mocker, cli_runner, mocked_fasjson_proxy):
    configure_cache = mocker.patch("fmn.cache.cli.configure_cache")
    get_value = mocker.patch.object(TrackedCache, "get_value")
    get_value.return_value = {"foo": "bar"}
    mocker.patch("fmn.cache.cli.init_async_model")

    result = cli_runner.invoke(cli, ["cache", "get-tracked"])

    assert result.exit_code == 0, result.output
    configure_cache.assert_called_once_with()
    get_value.assert_called_once()
    assert result.output == "{'foo': 'bar'}\n"


def test_delete_tracked(mocker, cli_runner):
    configure_cache = mocker.patch("fmn.cache.cli.configure_cache")
    get_value = mocker.patch.object(TrackedCache, "get_value")
    get_value.return_value = {"foo": "bar"}
    invalidate_tracked = mocker.patch.object(TrackedCache, "invalidate")

    result = cli_runner.invoke(cli, ["cache", "delete-tracked"])

    assert result.exit_code == 0, result.output
    configure_cache.assert_called_once_with()
    invalidate_tracked.assert_called_once_with()


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
