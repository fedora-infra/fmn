# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
import logging
import sys
import traceback

import backoff
from fastapi.concurrency import run_in_threadpool
from fedora_messaging import api
from fedora_messaging import exceptions as fm_exceptions

log = logging.getLogger(__name__)


def backoff_hdlr(details):
    log.warning("Publishing message failed. Retrying. %s", traceback.format_tb(sys.exc_info()[2]))


def giveup_hdlr(details):
    log.error("Publishing message failed. Giving up. %s", traceback.format_tb(sys.exc_info()[2]))


@backoff.on_exception(
    backoff.expo,
    (fm_exceptions.ConnectionException, fm_exceptions.PublishException),
    max_tries=3,
    on_backoff=backoff_hdlr,
    on_giveup=giveup_hdlr,
)
def _publish(message):
    api.publish(message)


_background_tasks = set()


async def publish(message):
    # Fire and forget
    # https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task
    task = asyncio.create_task(run_in_threadpool(_publish, message=message))
    _background_tasks.add(task)
    # To prevent keeping references to finished tasks forever, make each task
    # remove its own reference from the set after completion:
    task.add_done_callback(_background_tasks.discard)
