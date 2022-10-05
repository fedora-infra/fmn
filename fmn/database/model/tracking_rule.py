from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..main import Base
from .rule import Rule


class TrackingRule(Base):
    __tablename__ = "tracking_rules"

    id = Column(Integer, primary_key=True, nullable=False)

    # Unique: there can be only one TrackingRule per Rule
    rule_id = Column(Integer, ForeignKey(Rule.id), nullable=False, unique=True)
    rule = relationship(Rule, back_populates="tracking_rule", uselist=False)

    name = Column(String(length=255), nullable=False)
    params = Column(JSON)
