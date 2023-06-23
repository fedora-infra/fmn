# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
from functools import cached_property


class Handler:
    def __init__(self, config):
        self._config = config

    async def setup(self):
        # Here we connect to the destination server if relevant.
        ...

    async def stop(self):
        ...

    @cached_property
    def closed(self):
        """Default `closed` Future, can be overridden in child classes.

        It should be triggered when there is an error and the app should stop.
        """
        return asyncio.get_event_loop().create_future()  # pragma: no cover

    async def handle(self, message):
        raise NotImplementedError


class HandlerError(Exception):
    pass


class PrintHandler(Handler):
    async def handle(self, message):
        print("Received:", message)  # pragma: no cover
