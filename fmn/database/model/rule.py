from sqlalchemy import Column, ForeignKey, Integer, UnicodeText
from sqlalchemy.orm import relationship

from ..main import Base
from .user import User


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, nullable=False)

    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    user = relationship(User, back_populates="rules")

    tracking_rule = relationship(
        "TrackingRule", back_populates="rule", uselist=False, cascade="all, delete-orphan"
    )
    generation_rules = relationship(
        "GenerationRule", back_populates="rule", cascade="all, delete-orphan"
    )
