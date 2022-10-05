import logging
from typing import Any

from pydantic import BaseModel
from pydantic.utils import GetterDict

log = logging.getLogger(__name__)


class TrackingRule(BaseModel):
    name: str
    params: list[str] | dict[str, str] | None

    class Config:
        orm_mode = True


class Destination(BaseModel):
    protocol: str
    address: str

    class Config:
        orm_mode = True


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
        orm_mode = True
        getter_dict = GRGetterDict


class Rule(BaseModel):
    id: int | None
    name: str
    tracking_rule: TrackingRule
    generation_rules: list[GenerationRule]

    class Config:
        orm_mode = True
