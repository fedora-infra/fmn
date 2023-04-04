# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from functools import cache
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, UnicodeText, select
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.sql import Select, expression

from ..main import Base
from .generated import Generated
from .generation_rule import GenerationRule
from .tracking_rule import TrackingRule
from .user import User

if TYPE_CHECKING:
    from fedora_messaging.message import Message

    from ...rules.requester import Requester


log = logging.getLogger(__name__)


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, nullable=True)
    disabled = Column(
        Boolean, default=False, nullable=False, index=True, server_default=expression.text("FALSE")
    )

    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    user = relationship(User, back_populates="rules")

    tracking_rule = relationship(
        TrackingRule, back_populates="rule", uselist=False, cascade="all, delete-orphan"
    )
    generation_rules = relationship(
        GenerationRule, back_populates="rule", cascade="all, delete-orphan"
    )
    generated = relationship(Generated, back_populates="rule", cascade="all, delete-orphan")

    @classmethod
    @cache
    def select_related(cls) -> Select:
        """Convenience method to query rules and related property objects.

        This tells SQLAlchemy to query ORM objects related to a Rule right in
        the query which is necessary when accessing their respective properties
        in an async context.
        """
        return select(cls).options(
            selectinload(cls.user),
            selectinload(cls.tracking_rule),
            selectinload(cls.generation_rules),
            selectinload(cls.generation_rules).selectinload(GenerationRule.destinations),
            selectinload(cls.generation_rules).selectinload(GenerationRule.filters),
        )

    async def handle(self, message: "Message", requester: "Requester"):
        log.debug("Rule %s handling message %s", self.id, message.id)
        if not await self.tracking_rule.matches(message, requester):
            return
        for generation_rule in self.generation_rules:
            async for notification in generation_rule.handle(message, requester):
                yield notification
