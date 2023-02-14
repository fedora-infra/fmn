from datetime import timedelta
from functools import cache
from typing import Any

from pydantic import BaseModel, BaseSettings, root_validator, stricturl

DEFAULT_CONFIG_FILE = _settings_file = "/etc/fmn/fmn.cfg"

CashewsTTLTypes = int | float | str | timedelta


class CacheArgsModel(BaseModel):
    ttl: CashewsTTLTypes | None = None
    early_ttl: CashewsTTLTypes | None = None

    class Config:
        extra = "allow"


class CacheScopedArgsModel(BaseModel):
    tracked: CacheArgsModel = CacheArgsModel(ttl="1d", early_ttl="22h")
    rules: CacheArgsModel = CacheArgsModel(ttl="1d", early_ttl="22h")
    pagure: CacheArgsModel | None = None
    fasjson: CacheArgsModel | None = None


class CacheModel(BaseModel):
    url: stricturl(tld_required=False, host_required=False) = "mem://"
    setup_args: dict[str, Any] | None = None

    default_args: CacheArgsModel = CacheArgsModel(ttl="1h")
    scoped_args: CacheScopedArgsModel = CacheScopedArgsModel()


class SQLAlchemyModel(BaseModel):
    url: stricturl(tld_required=False, host_required=False) = "sqlite:///:memory:"
    echo: bool = False

    class Config:
        extra = "allow"


class DBModel(BaseModel):
    sqlalchemy: SQLAlchemyModel = SQLAlchemyModel()


class ServicesModel(BaseModel):
    fasjson_url: stricturl() = "https://fasjson.fedoraproject.org"
    distgit_url: stricturl() = "https://src.fedoraproject.org"
    datagrepper_url: stricturl() = "https://apps.fedoraproject.org/datagrepper/"


class Settings(BaseSettings):
    cors_origins: str = "https://notifications.fedoraproject.org"
    oidc_provider_url: str = "https://id.fedoraproject.org/openidc"
    oidc_conf_endpoint: str = "/.well-known/openid-configuration"
    oidc_token_info_endpoint: str = "/TokenInfo"
    oidc_client_id: str = "0123456789abcdef0123456789abcdef"
    oidc_client_secret: str = "0123456789abcdef0123456789abcdef"

    # these fields are computed from the above
    oidc_conf_url: str | None
    oidc_token_info_url: str | None

    id_cache_gc_interval: int = 300

    database: DBModel = DBModel()
    cache: CacheModel = CacheModel()
    services: ServicesModel = ServicesModel()

    class Config:
        env_file = "fmn.cfg"
        env_nested_delimiter = "__"

    @root_validator
    def compute_compound_fields(cls, values) -> dict:
        values["oidc_conf_url"] = (
            values["oidc_provider_url"].rstrip("/") + "/" + values["oidc_conf_endpoint"].lstrip("/")
        )
        values["oidc_token_info_url"] = (
            values["oidc_provider_url"].rstrip("/")
            + "/"
            + values["oidc_token_info_endpoint"].lstrip("/")
        )
        return values


@cache
def get_settings() -> Settings:
    return Settings(_env_file=_settings_file)


def set_settings_file(path: str) -> None:
    global _settings_file
    _settings_file = path
    get_settings.cache_clear()
