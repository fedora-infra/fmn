from importlib.metadata import entry_points

import click
import click_plugins

from . import config
from .version import __version__


@click_plugins.with_plugins(entry_points(group="fmn.cli"))
@click.group(name="fmn")
@click.option(
    "settings_file",
    "--config",
    "-c",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="The configuration file for FMN.",
)
@click.version_option(version=__version__, prog_name="FMN")
def cli(settings_file: str | None):
    """Fedora Messaging Notifications"""
    if settings_file:
        config.set_settings_file(settings_file)
