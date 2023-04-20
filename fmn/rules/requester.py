# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from typing import TYPE_CHECKING

from ..backends import FASJSONAsyncProxy, PagureAsyncProxy

if TYPE_CHECKING:
    from fedora_messaging.message import Message
    from sqlalchemy.ext.asyncio import AsyncSession


log = logging.getLogger(__name__)


class Requester:
    def __init__(self, config):
        self.distgit = PagureAsyncProxy(config.distgit_url)
        self.fasjson = FASJSONAsyncProxy(config.fasjson_url)

    async def invalidate_on_message(self, message: "Message", db: "AsyncSession"):
        await self.distgit.invalidate_on_message(message, db)
        await self.fasjson.invalidate_on_message(message, db)
