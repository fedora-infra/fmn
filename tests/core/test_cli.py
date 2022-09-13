from unittest import mock

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
