# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
import re
from typing import Annotated, Generic, Literal, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, field_validator, model_validator
from pydantic_core.core_schema import FieldValidationInfo

from ..core.constants import ArtifactType

log = logging.getLogger(__name__)


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)


# Tracking rules with specific types for params


class ListParamTrackingRule(BaseModel):
    name: Literal["artifacts-owned", "artifacts-group-owned", "users-followed"]
    params: list[str]


class NoParamTrackingRule(BaseModel):
    name: Literal["related-events"]
    params: str | None = None


class ArtifactsFollowedTrackingRule(BaseModel):
    name: Literal["artifacts-followed"]
    params: list[dict[Literal["name", "type"], str]]


TrackingRule = Annotated[
    ListParamTrackingRule | NoParamTrackingRule | ArtifactsFollowedTrackingRule,
    Field(discriminator="name"),
]


# DB models

EMAIL_ADDRESS_RE = re.compile(r"[\w_.+-]+@[\w.-]+")
MATRIX_ADDRESS_RE = re.compile(r"@[\w_-]+:[\w.-]+")


class Destination(BaseModel):
    protocol: str
    address: str

    @field_validator("address")
    def address_format(cls, v, info: FieldValidationInfo):
        if info.data["protocol"] == "email" and not EMAIL_ADDRESS_RE.match(v):
            message = f"The email address {v!r} does not look right"
            log.warning(message)
            raise ValueError(message)
        elif info.data["protocol"] == "matrix" and not MATRIX_ADDRESS_RE.match(v):
            message = f"The Matrix address {v!r} should be in the form @username:server.tld"
            log.warning(message)
            raise ValueError(message)
        return v


class Filters(BaseModel):
    applications: list[str] = []
    severities: list[str] = []
    topic: str | None = None
    my_actions: bool = False

    @model_validator(mode="before")
    def convert_from_orm(cls, data):
        if isinstance(data, list):
            return {f.name: f.params for f in data}
        return data


class GenerationRule(BaseModel):
    id: int | None = None
    destinations: list[Destination]
    filters: Filters


class User(BaseModel):
    id: int | None = None
    name: str
    is_admin: bool = False


class NewRule(BaseModel):
    name: str | None = None
    disabled: bool = False
    tracking_rule: TrackingRule
    generation_rules: list[GenerationRule]


class Rule(NewRule):
    id: int
    user: User
    generated_last_week: int = 0


class RulePatch(BaseModel):
    disabled: bool | None = None


# Dropdown options

T = TypeVar("T")


class Option(BaseModel, Generic[T]):
    label: str
    value: T


class Artifact(BaseModel):
    type: ArtifactType
    name: str


class ArtifactOptionsGroup(BaseModel):
    label: str
    options: list[Option[Artifact]]
