# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel


class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class EmailNotificationHeaders(FrozenModel):
    To: str
    Subject: str


class EmailNotificationContent(FrozenModel):
    headers: EmailNotificationHeaders
    body: str


class EmailNotification(FrozenModel):
    protocol: Literal["email"]
    content: EmailNotificationContent


class IRCNotificationContent(FrozenModel):
    to: str
    message: str


class IRCNotification(FrozenModel):
    protocol: Literal["irc"]
    content: IRCNotificationContent


class MatrixNotificationContent(FrozenModel):
    to: str
    message: str


class MatrixNotification(FrozenModel):
    protocol: Literal["matrix"]
    content: MatrixNotificationContent


class Notification(RootModel):
    model_config = ConfigDict(frozen=True)
    root: Annotated[
        EmailNotification | IRCNotification | MatrixNotification, Field(discriminator="protocol")
    ]

    def __getattr__(self, attr):
        return getattr(self.root, attr)
