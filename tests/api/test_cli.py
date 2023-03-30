# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest import mock

from fmn.api import main
from fmn.api.cli import api


@api.command("test")
def _api_test():
    pass


@mock.patch("fmn.api.cli.verify_db_url_not_default")
def test_api(verify_db_url_not_default, cli_runner):
    cli_runner.invoke(api, "test")
    verify_db_url_not_default.assert_called_once_with()


@mock.patch("fmn.api.cli.verify_db_url_not_default", new=mock.Mock())
def test_api_help(cli_runner):
    result = cli_runner.invoke(api, ["--help"])
    assert result.exit_code == 0
    assert "Usage: api" in result.output


@mock.patch("fmn.api.cli.verify_db_url_not_default", new=mock.Mock())
@mock.patch("fmn.api.cli.uvicorn")
def test_api_serve(uvicorn, cli_runner):
    result = cli_runner.invoke(api, ["serve"])
    assert result.exit_code == 0
    uvicorn.run.assert_called_once_with(main.app, host="127.0.0.1", port=8080)
