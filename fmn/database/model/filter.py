# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from importlib.metadata import entry_points
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..main import Base
from .generation_rule import GenerationRule

if TYPE_CHECKING:
    from fedora_messaging.message import Message

    from ...rules.requester import Requester


class Filter(Base):
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True, nullable=False)

    generation_rule_id = Column(
        Integer, ForeignKey(GenerationRule.id, ondelete="CASCADE"), nullable=False
    )
    generation_rule = relationship(GenerationRule, back_populates="filters")

    name = Column(String(length=255), nullable=False)
    params = Column(JSON)

    def get_implementation(self, requester: "Requester"):
        eps = entry_points(group="fmn.filters", name=self.name)
        if len(eps) != 1:
            raise ValueError(f"Unknown filter: {self.name}")
        impl_class = eps[self.name].load()
        username = self.generation_rule.rule.user.name
        return impl_class(requester=requester, params=self.params, username=username)

    def matches(self, message: "Message", requester: "Requester"):
        impl = self.get_implementation(requester)
        return impl.matches(message)
