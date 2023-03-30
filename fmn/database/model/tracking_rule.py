# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from importlib.metadata import entry_points
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..main import Base

if TYPE_CHECKING:
    from fedora_messaging.message import Message

    from ...rules.requester import Requester


class TrackingRule(Base):
    __tablename__ = "tracking_rules"

    id = Column(Integer, primary_key=True, nullable=False)

    # Unique: there can be only one TrackingRule per Rule
    rule_id = Column(Integer, ForeignKey("rules.id"), nullable=False, unique=True)
    rule = relationship("Rule", back_populates="tracking_rule", uselist=False)

    name = Column(String(length=255), nullable=False)
    params = Column(JSON)

    def get_implementation(self, requester: "Requester"):
        eps = entry_points(group="fmn.tracking_rules", name=self.name)
        if len(eps) != 1:
            raise ValueError(f"Unknown tracking rule: {self.name}")
        impl_class = eps[self.name].load()
        owner = self.rule.user.name
        return impl_class(requester, self.params, owner)

    async def matches(self, message: "Message", requester: "Requester"):
        impl = self.get_implementation(requester)
        return await impl.matches(message)

    async def prime_cache(self, cache, requester: "Requester"):
        impl = self.get_implementation(requester)
        return await impl.prime_cache(cache)
