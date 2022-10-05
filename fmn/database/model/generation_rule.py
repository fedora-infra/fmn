from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from ..main import Base
from .rule import Rule


class GenerationRule(Base):
    __tablename__ = "generation_rules"

    id = Column(Integer, primary_key=True, nullable=False)

    rule_id = Column(Integer, ForeignKey(Rule.id, ondelete="CASCADE"), nullable=False)
    rule = relationship(Rule, back_populates="generation_rules")

    destinations = relationship(
        "Destination", back_populates="generation_rule", cascade="all, delete-orphan"
    )
    filters = relationship(
        "Filter",
        back_populates="generation_rule",
        cascade="all, delete-orphan",
        # collection_class=attribute_mapped_collection("name"),
    )
