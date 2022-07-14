from unittest import mock

from fmn.api import main
from fmn.api.cli import api


def test_api_help(cli_runner):
    result = cli_runner.invoke(api, ["--help"])
    assert result.exit_code == 0
    assert "Usage: api" in result.output


@mock.patch("fmn.api.cli.uvicorn")
def test_api_serve(uvicorn, cli_runner):
    result = cli_runner.invoke(api, ["serve"])
    assert result.exit_code == 0
    uvicorn.run.assert_called_once_with(main.api)
