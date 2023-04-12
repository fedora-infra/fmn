# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
from functools import partial

import click

from .config import get_config, get_handler, setup_logging
from .consumer import Consumer


def shutdown(result, consumer):
    if asyncio.isfuture(result):
        result = result.result()
    click.echo(f"Shutting down: {result}")
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(consumer.stop())
    else:
        loop.run_until_complete(consumer.stop())


async def _main(handler, consumer):
    await handler.setup()
    # Shutdown in case of unexpected disconnections
    handler.closed.add_done_callback(partial(shutdown, consumer=consumer))
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
        shutdown("exception caught", consumer)
        raise click.ClickException(e) from e
