from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..main import Base
from .generation_rule import GenerationRule


class Filter(Base):
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True, nullable=False)

    generation_rule_id = Column(Integer, ForeignKey(GenerationRule.id), nullable=False)
    generation_rule = relationship(GenerationRule, backref="filters")

    name = Column(String(length=255), nullable=False)
    params = Column(JSON)
