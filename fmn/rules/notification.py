from typing import Annotated, Literal, TypedDict

from pydantic import BaseModel, Field


class EmailNotificationHeaders(TypedDict):
    To: str
    Subject: str


class EmailNotificationContent(BaseModel):
    headers: EmailNotificationHeaders
    body: str


class EmailNotification(BaseModel):
    protocol: Literal["email"]
    content: EmailNotificationContent


class IRCNotificationContent(BaseModel):
    to: str
    message: str


class IRCNotification(BaseModel):
    protocol: Literal["irc"]
    content: IRCNotificationContent


class MatrixNotificationContent(BaseModel):
    to: str
    message: str


class MatrixNotification(BaseModel):
    protocol: Literal["matrix"]
    content: MatrixNotificationContent


class Notification(BaseModel):
    __root__: Annotated[
        EmailNotification | IRCNotification | MatrixNotification, Field(discriminator="protocol")
    ]

    def __getattr__(self, attr):
        return getattr(self.__root__, attr)
