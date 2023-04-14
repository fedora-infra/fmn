# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
from textwrap import dedent
from unittest.mock import AsyncMock, MagicMock

import pytest
from click.testing import CliRunner

from fmn.sender import cli
from fmn.sender.consumer import Consumer
from fmn.sender.handler import Handler, HandlerError


@pytest.fixture
def config_file(tmp_path):
    config_path = tmp_path.joinpath("config.toml")
    with open(config_path, "w") as config_fh:
        config_fh.write(
            dedent(
                """
        amqp_url = "amqp://localhost/%2Ffmn"
        queue = "email"

        [handler]
        class = "fmn.sender.email:EmailHandler"
        from = "Test <test@example.com>"
        smtp_host = "smtp.example.com"
        smtp_port = 487
        """
            )
        )
    return config_path


@pytest.fixture
def mocked_handler(mocker):
    handler = MagicMock(spec=Handler)
    handler.closed = asyncio.get_event_loop().create_future()
    mocker.patch("fmn.sender.cli.get_handler", return_value=handler)
    return handler


@pytest.fixture
def mocked_consumer(mocker):
    consumer = MagicMock(spec=Consumer)
    mocker.patch("fmn.sender.cli.Consumer", return_value=consumer)
    return consumer


def test_cli(config_file, mocked_handler, mocked_consumer):
    runner = CliRunner()
    result = runner.invoke(cli.main, ["-c", config_file])

    mocked_handler.setup.assert_awaited_once_with()
    mocked_consumer.connect.assert_awaited_once_with()
    mocked_consumer.start.assert_awaited_once_with()
    assert result.exit_code == 0
    assert result.output == ""


def test_cli_keyboardinterrupt(config_file, mocked_handler, mocked_consumer):
    mocked_consumer.start = AsyncMock(side_effect=KeyboardInterrupt)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["-c", config_file])

    assert result.exit_code == 1
    assert result.output == "\nAborted!\n"


def test_cli_generic_error(config_file, mocked_handler, mocked_consumer):
    mocked_consumer.start = AsyncMock(side_effect=RuntimeError("dummy error"))

    runner = CliRunner()
    result = runner.invoke(cli.main, ["-c", config_file])

    assert result.exit_code == 1
    assert result.output == "Shutting down: exception caught\nError: dummy error\n"
    mocked_consumer.stop.assert_awaited_once_with()


def test_cli_handler_setup_error(config_file, mocked_handler, mocked_consumer):
    mocked_handler.setup = AsyncMock(side_effect=HandlerError("dummy error"))

    runner = CliRunner()
    result = runner.invoke(cli.main, ["-c", config_file])

    assert result.exit_code == 1
    expected = "Shutting down: exception caught\nError: dummy error\n"
    assert result.output == expected
    mocked_consumer.stop.assert_awaited_once_with()


def test_cli_handler_setup_timeout(config_file, mocker, mocked_handler, mocked_consumer):
    async def _wait():
        await asyncio.sleep(10)

    mocker.patch("fmn.sender.cli.HANDLER_CONNECT_TIMEOUT", 0.5)
    mocked_handler.setup = AsyncMock(side_effect=_wait)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["-c", config_file])

    assert result.exit_code == 1
    expected = "Shutting down: exception caught\nError: the handler could not connect in 0.5s\n"
    assert result.output == expected
    mocked_consumer.stop.assert_awaited_once_with()


def test_cli_handler_closed(config_file, mocker, mocked_handler, mocked_consumer):
    async def _close():
        mocked_handler.closed.set_result("dummy close")
        # give it time to call consumer.stop()
        await asyncio.sleep(1)

    mocked_consumer.start = AsyncMock(side_effect=_close)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["-c", config_file])

    assert result.output == "Shutting down: dummy close\n"
    mocked_consumer.stop.assert_awaited_once_with()
