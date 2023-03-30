# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from sqlalchemy import Column, Integer, UnicodeText
from sqlalchemy.orm import relationship

from ..main import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, nullable=False, unique=True)

    rules = relationship("Rule", back_populates="user")
