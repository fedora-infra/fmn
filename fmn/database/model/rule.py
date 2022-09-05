from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..main import Base
from .user import User


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, nullable=False)

    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship(User, backref="rules")
