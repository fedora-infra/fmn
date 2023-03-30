# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText
from sqlalchemy.orm import relationship

from ..main import Base
from .generation_rule import GenerationRule

if TYPE_CHECKING:
    from fedora_messaging.message import Message

    from ...rules.notification import Notification


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, nullable=False)

    generation_rule_id = Column(
        Integer, ForeignKey(GenerationRule.id, ondelete="CASCADE"), nullable=False
    )
    generation_rule = relationship(GenerationRule, back_populates="destinations")

    protocol = Column(String(length=255), nullable=False)
    address = Column(UnicodeText, nullable=False)

    def generate(self, message: "Message") -> "Notification.content":
        app_name = f"[{message.app_name}] " if message.app_name else ""
        url = message.url if message.url else ""
        if self.protocol == "email":
            return {
                "headers": {
                    "To": self.address,
                    "Subject": f"{app_name}{message.summary}",
                },
                "body": f"{str(message)}\n{url}",
            }
        elif self.protocol == "irc":
            return {"to": self.address, "message": f"{app_name}{message.summary} {url}"}
        elif self.protocol == "matrix":
            return {"to": self.address, "message": f"{app_name}{message.summary} {url}"}
        else:
            raise ValueError(f"Unknown destination protocol: {self.protocol}")
