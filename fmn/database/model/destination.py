# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from typing import TYPE_CHECKING

from httpx import AsyncClient, HTTPStatusError
from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText, select
from sqlalchemy.ext.asyncio import async_object_session
from sqlalchemy.orm import relationship

from ...core.config import get_settings
from ..main import Base
from .generation_rule import GenerationRule

if TYPE_CHECKING:
    from fedora_messaging.message import Message

    from ...rules.notification import Notification


log = logging.getLogger(__name__)


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, nullable=False)

    generation_rule_id = Column(
        Integer, ForeignKey(GenerationRule.id, ondelete="CASCADE"), nullable=False
    )
    generation_rule = relationship(GenerationRule, back_populates="destinations")

    protocol = Column(String(length=255), nullable=False)
    address = Column(UnicodeText, nullable=False)

    async def generate(self, message: "Message") -> "Notification.content":
        app_name = f"[{message.app_name}] " if message.app_name else ""
        url = message.url if message.url else ""
        settings = get_settings()
        if self.protocol == "email":
            body = f"{message!s}\n{url}"
            extra = await get_extra(message)
            if extra:
                body = f"{body}\n{extra}"

            # Find the URL of the Rule that generated this notification
            session = async_object_session(self)
            result = await session.execute(
                select(GenerationRule).where(GenerationRule.id == self.generation_rule_id)
            )
            rule_id = result.scalar_one().rule_id
            return {
                "headers": {
                    "To": self.address,
                    "Subject": f"{app_name}{message.summary}",
                },
                "body": body,
                "footer": f"Sent by Fedora Notifications: {settings.public_url}/rules/{rule_id}",
            }
        elif self.protocol == "irc":
            return {"to": self.address, "message": f"{app_name}{message.summary} {url}"}
        elif self.protocol == "matrix":
            return {"to": self.address, "message": f"{app_name}{message.summary} {url}"}
        else:
            raise ValueError(f"Unknown destination protocol: {self.protocol}")


async def get_extra(message: "Message"):
    http_client = AsyncClient(timeout=10)
    if getattr(message, "patch_url", None) is not None:
        try:
            response = await http_client.get(message.patch_url)
            response.raise_for_status()
        except HTTPStatusError as e:
            log.info(f"Could not retrieve patch at {message.patch_url}: {e}")
        else:
            return f"\n{response.text}\n"
    return ""
