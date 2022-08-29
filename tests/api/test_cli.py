from unittest import mock

import pytest

from fmn.api import cli, config, main
from fmn.api.cli import api


def test_api_help(cli_runner):
    result = cli_runner.invoke(api, ["--help"])
    assert result.exit_code == 0
    assert "Usage: api" in result.output


@pytest.mark.parametrize("default_config", (True, False))
@mock.patch.object(config, "settings_file")
def test_api_settings(settings_file, default_config, cli_runner):
    if default_config:
        args = []
    else:
        args = [f"--config={__file__}"]

    with mock.patch("fmn.api.config.get_settings") as get_settings:
        result = cli_runner.invoke(api, args + ["test-helper"])
        get_settings.cache_clear.assert_called_once_with()

    assert result.exit_code == 0
    if default_config:
        assert config.settings_file == cli.DEFAULT_CONFIG_FILE
    else:
        assert config.settings_file == __file__


@mock.patch("fmn.api.cli.uvicorn")
def test_api_serve(uvicorn, cli_runner):
    result = cli_runner.invoke(api, ["serve"])
    assert result.exit_code == 0
    uvicorn.run.assert_called_once_with(main.app, host="127.0.0.1")
