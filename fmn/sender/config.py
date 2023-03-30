# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
import logging.config
from importlib import import_module

import tomli

_log = logging.getLogger(__name__)


DEFAULTS = dict(
    amqp_url="amqp://?connection_attempts=3&retry_delay=5",
    queue="fmn",
    handler={
        "class": "fmn.sender.handler:PrintHandler",
    },
    log_config={
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"simple": {"format": "[%(name)s %(levelname)s] %(message)s"}},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "fmn": {
                "level": "INFO",
                "propagate": False,
                "handlers": ["console"],
            }
        },
        # The root logger configuration; this is a catch-all configuration
        # that applies to all log messages not handled by a different logger
        "root": {"level": "WARNING", "handlers": ["console"]},
    },
)


def get_config(path):
    with open(path, "rb") as fh:
        config = tomli.load(fh)
    for key, value in DEFAULTS.items():
        if key not in config:
            config[key] = value
    return config


def get_handler(config):
    handler_module_path, handler_class_name = config["handler"]["class"].split(":", 1)
    handler_module = import_module(handler_module_path)
    handler_class = getattr(handler_module, handler_class_name)
    return handler_class(config["handler"])


def setup_logging(config):
    logging.config.dictConfig(config["log_config"])
