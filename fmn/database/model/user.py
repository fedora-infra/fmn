from sqlalchemy import Column, Integer, UnicodeText

from ..main import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, nullable=False, unique=True)
