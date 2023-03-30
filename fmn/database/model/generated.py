# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from ..main import Base


class Generated(Base):
    __tablename__ = "generated"

    id = Column(Integer, primary_key=True, nullable=False)

    rule_id = Column(Integer, ForeignKey("rules.id", ondelete="CASCADE"), nullable=False)
    rule = relationship("Rule", back_populates="generated")

    when = Column(
        DateTime(timezone=False),
        index=True,
        default=datetime.now,
        server_default=func.now(),
        nullable=False,
    )
    count = Column(Integer, default=0)
