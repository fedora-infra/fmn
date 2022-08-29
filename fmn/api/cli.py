import click
import uvicorn

from . import config, main

DEFAULT_CONFIG_FILE = "/etc/fmn/api.cfg"


@click.group()
@click.option(
    "settings_file",
    "--config",
    "-c",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="The configuration file for the API service.",
)
def api(settings_file: str | None):
    """The FMN API service"""
    config.settings_file = settings_file or DEFAULT_CONFIG_FILE
    config.get_settings.cache_clear()


@api.command(hidden=True)
def test_helper():
    pass


@api.command()
@click.option("--host", default="127.0.0.1", help="host to serve the api on")
def serve(host):
    """Serve the FMN API via HTTP"""
    uvicorn.run(main.app, host=host)
