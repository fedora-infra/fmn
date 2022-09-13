from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..main import Base
from .rule import Rule


class GenerationRule(Base):
    __tablename__ = "generation_rules"

    id = Column(Integer, primary_key=True, nullable=False)

    rule_id = Column(Integer, ForeignKey(Rule.id), nullable=False)
    rule = relationship(Rule, backref="generation_rules")
