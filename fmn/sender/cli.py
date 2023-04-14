# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio

import click

from .config import get_config, get_handler, setup_logging
from .consumer import Consumer
from .handler import HandlerError

HANDLER_CONNECT_TIMEOUT = 60


async def _shutdown(result, consumer):
    if asyncio.isfuture(result):
        result = await result
    click.echo(f"Shutting down: {result}")
    await consumer.stop()


background_tasks = set()


async def _main(handler, consumer):
    try:
        await asyncio.wait_for(handler.setup(), timeout=HANDLER_CONNECT_TIMEOUT)
    except asyncio.exceptions.TimeoutError as e:
        raise HandlerError(f"the handler could not connect in {HANDLER_CONNECT_TIMEOUT}s") from e

    # Shutdown in case of unexpected disconnections
    shutdown_on_closed = asyncio.create_task(_shutdown(handler.closed, consumer))
    # Trick Python into creating a strong reference
    # https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task
    background_tasks.add(shutdown_on_closed)
    shutdown_on_closed.add_done_callback(background_tasks.discard)

    await consumer.connect()
    await consumer.start()


@click.command()
@click.option(
    "-c",
    "--config",
    "config_path",
    required=True,
    help="Path to the configuration file (in TOML format)",
)
def main(config_path):
    config = get_config(config_path)
    setup_logging(config)
    handler = get_handler(config)
    consumer = Consumer(config, handler)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_main(handler, consumer))
    except Exception as e:
        loop.run_until_complete(_shutdown("exception caught", consumer))
        raise click.ClickException(e) from e
