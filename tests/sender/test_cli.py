from textwrap import dedent
from unittest.mock import AsyncMock, MagicMock

import pytest
from click.testing import CliRunner

from fmn.sender import cli
from fmn.sender.consumer import Consumer
from fmn.sender.handler import Handler


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


def test_cli(config_file, mocker):
    mocked_handler = MagicMock(spec=Handler)
    mocker.patch("fmn.sender.cli.get_handler", return_value=mocked_handler)
    mocked_consumer = MagicMock(spec=Consumer)
    mocker.patch("fmn.sender.cli.Consumer", return_value=mocked_consumer)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["-c", config_file])

    mocked_handler.setup.assert_called_once_with()
    mocked_consumer.connect.assert_called_once_with()
    mocked_consumer.start.assert_called_once_with()
    assert result.exit_code == 0
    assert result.output == ""


def test_cli_keyboardinterrupt(config_file, mocker):
    mocked_handler = MagicMock(spec=Handler)
    mocker.patch("fmn.sender.cli.get_handler", return_value=mocked_handler)
    mocked_consumer = MagicMock(spec=Consumer)
    mocker.patch("fmn.sender.cli.Consumer", return_value=mocked_consumer)
    mocked_consumer.start = AsyncMock(side_effect=KeyboardInterrupt)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["-c", config_file])

    assert result.exit_code == 1
    assert result.output == "\nAborted!\n"
