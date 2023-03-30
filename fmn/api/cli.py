# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import click
import uvicorn

from ..database.cli import verify_db_url_not_default
from . import main


@click.group()
def api():
    """The FMN API service"""
    verify_db_url_not_default()


@api.command()
@click.option("--host", default="127.0.0.1", help="host to serve the api on")
@click.option("--port", default="8080", type=int, help="port to serve the api on")
def serve(host, port):
    """Serve the FMN API via HTTP"""
    uvicorn.run(main.app, host=host, port=port)
