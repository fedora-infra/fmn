from functools import cache

from sqlalchemy import Column, ForeignKey, Integer, UnicodeText, select
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.sql import Select

from ..main import Base
from .generation_rule import GenerationRule
from .tracking_rule import TrackingRule
from .user import User


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, nullable=False)

    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    user = relationship(User, back_populates="rules")

    tracking_rule = relationship(
        TrackingRule, back_populates="rule", uselist=False, cascade="all, delete-orphan"
    )
    generation_rules = relationship(
        GenerationRule, back_populates="rule", cascade="all, delete-orphan"
    )

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
            selectinload(cls.generation_rules, GenerationRule.destinations),
            selectinload(cls.generation_rules, GenerationRule.filters),
        )
