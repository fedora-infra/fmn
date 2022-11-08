from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText
from sqlalchemy.orm import relationship

from ..main import Base
from .generation_rule import GenerationRule

if TYPE_CHECKING:
    from fedora_messaging.message import Message


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, nullable=False)

    generation_rule_id = Column(
        Integer, ForeignKey(GenerationRule.id, ondelete="CASCADE"), nullable=False
    )
    generation_rule = relationship(GenerationRule, back_populates="destinations")

    protocol = Column(String(length=255), nullable=False)
    address = Column(UnicodeText, nullable=False)

    def generate(self, message: "Message"):
        if self.protocol == "email":
            return {
                "headers": {
                    "To": self.address,
                    "Subject": message.summary,
                },
                "body": str(message),
            }
        elif self.protocol == "irc":
            return {
                "to": self.address,
                "message": message.summary,
            }
        elif self.protocol == "preview":
            return {
                "date": message._headers.get("sent-at"),
                "topic": message.topic,
                "summary": message.summary,
                "priority": message.priority,
                "application": message.app_name,
                "author": message.agent_name,
            }
        else:
            raise ValueError(f"Unknown destination protocol: {self.protocol}")
