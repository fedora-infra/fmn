from importlib.metadata import entry_points

import click
import click_plugins

from . import config
from .version import __version__

DEFAULT_CONFIG_FILE = "/etc/fmn.cfg"


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
    config.settings_file = settings_file or DEFAULT_CONFIG_FILE
    config.get_settings.cache_clear()
