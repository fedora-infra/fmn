import sys

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points  # pragma: no cover
else:
    from importlib.metadata import entry_points  # pragma: no cover

import click
import click_plugins

from .version import __version__


@click_plugins.with_plugins(entry_points(group="fmn.cli"))
@click.group(name="fmn")
@click.version_option(version=__version__, prog_name="FMN")
def cli():
    """Fedora Messaging Notifications"""
