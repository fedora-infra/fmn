# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from cashews import cache

from .base import CachedValue
from .util import cache_ttl, lock_ttl

if TYPE_CHECKING:
    from fedora_messaging.message import Message
    from sqlalchemy.ext.asyncio import AsyncSession

    from ..rules.requester import Requester
    from .rules import RulesCache

log = logging.getLogger(__name__)


@dataclass
class Tracked:
    packages: set = field(default_factory=set)
    containers: set = field(default_factory=set)
    modules: set = field(default_factory=set)
    flatpaks: set = field(default_factory=set)
    usernames: set = field(default_factory=set)
    agent_name: set = field(default_factory=set)


class TrackedCache(CachedValue):
    """Used to quickly know whether we want to process an incoming message.

    It can be called outside of the message-processing loop to refresh the cache.

    Cases when the cache should be refreshed:
    - a rule is changed
    - a user is added or removed to/from a group
    - an artifact has their owners (users or groups) changed

    The Consumer listens to those events as messages on the bus.

    If this happens too frequently, we can just refresh after X minutes have passed and tell
    users that their changes will take X minutes to be active.
    """

    name = "tracked"

    def __init__(self, requester: "Requester", rules_cache: "RulesCache"):
        self._requester = requester
        self._rules_cache = rules_cache

    @cache.locked(key=name, ttl=lock_ttl(name))
    # Don't use the lock=True option of the decorator because it does not allow to set the ttl for
    # the lock itself.
    @cache(key=name, prefix="v1", ttl=cache_ttl(name))
    async def get_value(self, db: "AsyncSession"):
        return await self.compute_value(db=db)

    async def _compute_value(self, db: "AsyncSession"):
        tracked = Tracked()
        for rule in await self._rules_cache.get_rules(db=db):
            await rule.tracking_rule.prime_cache(tracked, self._requester)
        return tracked

    async def invalidate_on_message(self, message: "Message"):
        if (
            message.topic.endswith("fmn.rule.create.v1")
            or message.topic.endswith("fmn.rule.update.v1")
            or message.topic.endswith("fmn.rule.delete.v1")
        ):
            await self.invalidate()
