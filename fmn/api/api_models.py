import logging
from typing import Annotated, Any, Generic, Literal,  Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field
from pydantic.utils import GetterDict

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
    params: str


class ArtifactsFollowedTrackingRule(BaseModel):
    name: Literal["artifacts-followed"]
    params: list[dict[Literal["name", "type"], str]]


TrackingRule = Annotated[
    Union[ListParamTrackingRule, NoParamTrackingRule, ArtifactsFollowedTrackingRule],
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
    tracking_rule: TrackingRule
    generation_rules: list[GenerationRule]


class User(BaseModel):
    id: int | None
    name: str
