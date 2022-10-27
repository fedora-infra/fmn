import logging
from functools import cache
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, UnicodeText, select
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.sql import Select

from ..main import Base
from .generation_rule import GenerationRule
from .tracking_rule import TrackingRule
from .user import User

if TYPE_CHECKING:
    from fedora_messaging.message import Message

    from fmn.rules.requester import Requester


log = logging.getLogger(__name__)


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

    def handle(self, message: "Message", requester: "Requester"):
        log.debug(f"Rule {self.id} handling message {message.id}")
        if not self.tracking_rule.matches(message, requester):
            log.debug(f"Tracking rule {self.tracking_rule.name} did not match with {message.id}")
            return
        for generation_rule in self.generation_rules:
            yield from generation_rule.handle(message, requester)
