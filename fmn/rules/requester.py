# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from typing import TYPE_CHECKING

from ..backends import get_distgit_proxy, get_fasjson_proxy

if TYPE_CHECKING:
    from fedora_messaging.message import Message
    from sqlalchemy.ext.asyncio import AsyncSession


log = logging.getLogger(__name__)


class Requester:
    def __init__(self):
        self.distgit = get_distgit_proxy()
        self.fasjson = get_fasjson_proxy()

    async def start(self):
        await self.distgit.start()
        await self.fasjson.start()

    async def stop(self):
        await self.distgit.stop()
        await self.fasjson.stop()

    def __aenter__(self):
        return self.start()

    def __aexit__(self, exc_type, exc_value, traceback):
        return self.stop()

    async def invalidate_on_message(self, message: "Message", db: "AsyncSession"):
        await self.distgit.invalidate_on_message(message, db)
        await self.fasjson.invalidate_on_message(message, db)
