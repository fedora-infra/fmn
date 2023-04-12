# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio


class Handler:
    def __init__(self, config):
        self._config = config
        # Triggered when there is an error and the app should stop
        self.closed = asyncio.get_event_loop().create_future()

    async def setup(self):
        # Here we connect to the destination server if relevant.
        pass

    async def stop(self):
        pass

    async def handle(self, message):
        raise NotImplementedError


class PrintHandler(Handler):
    async def handle(self, message):
        print("Received:", message)
