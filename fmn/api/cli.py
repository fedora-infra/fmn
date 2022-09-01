import click
import uvicorn

from . import main


@click.group()
def api():
    """The FMN API service"""
    pass


@api.command()
@click.option("--host", default="127.0.0.1", help="host to serve the api on")
def serve(host):
    """Serve the FMN API via HTTP"""
    uvicorn.run(main.app, host=host)
