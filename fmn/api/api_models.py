import logging
from typing import Annotated, Any, Generic, Literal, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field
from pydantic.generics import GenericModel
from pydantic.utils import GetterDict

from fmn.core.constants import ArtifactType

log = logging.getLogger(__name__)


class BaseModel(PydanticBaseModel):
    class Config:
        orm_mode = True


# Tracking rules with specific types for params


class ListParamTrackingRule(BaseModel):
    name: Literal["artifacts-owned", "artifacts-group-owned", "users-followed"]
    params: list[str]


class NoParamTrackingRule(BaseModel):
    name: Literal["related-events"]
    params: str | None


class ArtifactsFollowedTrackingRule(BaseModel):
    name: Literal["artifacts-followed"]
    params: list[dict[Literal["name", "type"], str]]


TrackingRule = Annotated[
    ListParamTrackingRule | NoParamTrackingRule | ArtifactsFollowedTrackingRule,
    Field(discriminator="name"),
]


# DB models


class Destination(BaseModel):
    protocol: str
    address: str


class Filters(BaseModel):
    applications: list[str] = []
    severities: list[str] = []
    topic: str | None = None
    my_actions: bool = False


class GRGetterDict(GetterDict):
    def get(self, key: str, default: Any) -> Any:
        if key == "filters":
            return {f.name: f.params for f in self._obj.filters}
        return super().get(key, default)


class GenerationRule(BaseModel):
    destinations: list[Destination]
    filters: Filters

    class Config:
        getter_dict = GRGetterDict


class Rule(BaseModel):
    id: int | None
    name: str
    disabled: bool = False
    tracking_rule: TrackingRule
    generation_rules: list[GenerationRule]


class GenerationRulePreview(GenerationRule):
    destinations: list[Destination] = []


class RulePreview(Rule):
    name: str = "preview"
    generation_rules: list[GenerationRulePreview]


class User(BaseModel):
    id: int | None
    name: str


# Dropdown options

T = TypeVar("T")


class Option(GenericModel, Generic[T]):
    label: str
    value: T


class Artifact(BaseModel):
    type: ArtifactType
    name: str


class ArtifactOptionsGroup(BaseModel):
    label: str
    options: list[Option[Artifact]]
