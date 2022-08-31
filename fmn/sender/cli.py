import asyncio

import click

from .config import get_config, get_handler, setup_logging
from .consumer import Consumer


async def _main(handler, consumer):
    await handler.setup()
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
    consumer = Consumer(config["amqp_url"], config["queue"], handler)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_main(handler, consumer))
    except KeyboardInterrupt:
        loop.run_until_complete(consumer.stop())
        loop.close()
