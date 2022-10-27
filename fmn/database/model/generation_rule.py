from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from fmn.rules.notification import Notification

from ..main import Base

if TYPE_CHECKING:
    from fedora_messaging.message import Message

    from fmn.rules.requester import Requester


class GenerationRule(Base):
    __tablename__ = "generation_rules"

    id = Column(Integer, primary_key=True, nullable=False)

    rule_id = Column(Integer, ForeignKey("rules.id", ondelete="CASCADE"), nullable=False)
    rule = relationship("Rule", back_populates="generation_rules")

    destinations = relationship(
        "Destination", back_populates="generation_rule", cascade="all, delete-orphan"
    )
    filters = relationship(
        "Filter",
        back_populates="generation_rule",
        cascade="all, delete-orphan",
        # collection_class=attribute_mapped_collection("name"),
    )

    def handle(self, message: "Message", requester: "Requester"):
        filters = self.filters
        if filters and not all([f.matches(message, requester) for f in filters]):
            return
        for destination in self.destinations:
            yield Notification(protocol=destination.protocol, content=destination.generate(message))
