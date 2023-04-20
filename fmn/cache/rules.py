# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from typing import TYPE_CHECKING

from ..database.model import Rule
from .base import CachedValue

if TYPE_CHECKING:
    from fedora_messaging.message import Message
    from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)


class RulesCache(CachedValue):
    """Cache the rules currently in the database."""

    name = "rules"

    async def get_rules(self, db: "AsyncSession"):
        return [await db.merge(r) for r in await self.get_value(db=db)]

    async def _compute_value(self, db: "AsyncSession"):
        result = await db.execute(Rule.select_related().filter_by(disabled=False))
        return list(result.scalars())

    async def invalidate_on_message(self, message: "Message", db: "AsyncSession"):
        if (
            message.topic.endswith("fmn.rule.create.v1")
            or message.topic.endswith("fmn.rule.update.v1")
            or message.topic.endswith("fmn.rule.delete.v1")
        ):
            await self.invalidate(db)
