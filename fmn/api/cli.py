import click
import uvicorn

from . import main


@click.group()
def api():
    """The FMN API service"""


@api.command()
def serve():
    """Serve the FMN API via HTTP"""
    uvicorn.run(main.app)
