import click

from .config import get_config, get_handler, setup_logging
from .consumer import Consumer


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
    handler.setup()
    consumer = Consumer(config["amqp_url"], config["queue"], handler)
    consumer.connect()
    try:
        consumer.start()
    except KeyboardInterrupt:
        consumer.stop()
