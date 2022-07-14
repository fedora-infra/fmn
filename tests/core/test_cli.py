from fmn.core.cli import cli
from fmn.core.version import __version__


def test_cli_version(cli_runner):
    """Ensure `fmn --version` works."""
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.output == f"FMN, version {__version__}\n"


def test_cli_help(cli_runner):
    """Ensure `fmn --help` works."""
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage: fmn" in result.output
