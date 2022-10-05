from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText
from sqlalchemy.orm import relationship

from ..main import Base
from .generation_rule import GenerationRule


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, nullable=False)

    generation_rule_id = Column(
        Integer, ForeignKey(GenerationRule.id, ondelete="CASCADE"), nullable=False
    )
    generation_rule = relationship(GenerationRule, back_populates="destinations")

    protocol = Column(String(length=255), nullable=False)
    address = Column(UnicodeText, nullable=False)
