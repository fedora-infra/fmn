from unittest import mock

import pytest

from fmn.core import cli, config
from fmn.core.version import __version__


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


@pytest.mark.parametrize("default_config", (True, False))
@mock.patch.object(config, "settings_file")
def test_settings(settings_file, default_config, cli_runner):
    if default_config:
        args = []
    else:
        args = [f"--config={__file__}"]

    with mock.patch("fmn.core.config.get_settings") as get_settings:
        result = cli_runner.invoke(cli.cli, args + ["test"])
        get_settings.cache_clear.assert_called_once_with()

    assert result.exit_code == 0
    if default_config:
        assert config.settings_file == cli.DEFAULT_CONFIG_FILE
    else:
        assert config.settings_file == __file__
