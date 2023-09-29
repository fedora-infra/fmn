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
    footer: str | None = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.model_dump(exclude=["footer"]) == other.model_dump(exclude=["footer"])
        return super().__eq__(other)

    def __hash__(self):
        # Don't include the footer in the hash to be able to use set() to de-duplicate
        # notifications coming from different rules.
        internal_dict = self.__dict__.copy()
        del internal_dict["footer"]
        return hash(self.__class__) + hash(tuple(internal_dict.values()))


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
