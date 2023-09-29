# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from datetime import timedelta
from functools import cache
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, DirectoryPath, model_validator
from pydantic_settings import BaseSettings

DEFAULT_CONFIG_FILE = _settings_file = "/etc/fmn/fmn.cfg"
TOP_DIR = Path(__file__).parent.parent

CashewsTTLTypes = int | float | str | timedelta


class CacheArgsModel(BaseModel):
    ttl: CashewsTTLTypes | None = None
    lock_ttl: CashewsTTLTypes | None = None
    early_ttl: CashewsTTLTypes | None = None


class CacheScopedArgsModel(BaseModel):
    tracked: CacheArgsModel = CacheArgsModel(ttl="1d", lock_ttl="1h", early_ttl="20h")
    rules: CacheArgsModel = CacheArgsModel(ttl="1d", lock_ttl="5m", early_ttl="20h")
    pagure: CacheArgsModel | None = None
    fasjson: CacheArgsModel | None = None


class CacheModel(BaseModel):
    url: str = "mem://"
    setup_args: dict[str, Any] | None = None

    default_args: CacheArgsModel = CacheArgsModel(ttl="1h")
    scoped_args: CacheScopedArgsModel = CacheScopedArgsModel()


class SQLAlchemyModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    url: str = "sqlite:///:memory:"
    echo: bool = False
    isolation_level: str = "SERIALIZABLE"


class AlembicModel(BaseModel):
    migrations_path: DirectoryPath = TOP_DIR.joinpath("database").joinpath("migrations").absolute()


class DBModel(BaseModel):
    sqlalchemy: SQLAlchemyModel = SQLAlchemyModel()
    alembic: AlembicModel = AlembicModel()


class ServicesModel(BaseModel):
    fasjson_url: str = "https://fasjson.fedoraproject.org"
    distgit_url: str = "https://src.fedoraproject.org"


class Settings(BaseSettings):
    public_url: str = "https://notifications.fedoraproject.org"
    cors_origins: str = "https://notifications.fedoraproject.org"
    oidc_provider_url: str = "https://id.fedoraproject.org/openidc"
    oidc_conf_endpoint: str = "/.well-known/openid-configuration"
    oidc_token_info_endpoint: str = "/TokenInfo"
    oidc_user_info_endpoint: str = "/UserInfo"
    oidc_client_id: str = "0123456789abcdef0123456789abcdef"
    oidc_client_secret: str = "0123456789abcdef0123456789abcdef"

    admin_groups: list[str] = ["sysadmin-main"]

    # these fields are computed from the above
    oidc_conf_url: str | None = None
    oidc_token_info_url: str | None = None
    oidc_user_info_url: str | None = None

    id_cache_gc_interval: int = 300

    database: DBModel = DBModel()
    cache: CacheModel = CacheModel()
    services: ServicesModel = ServicesModel()

    model_config = ConfigDict(env_file="fmn.cfg", env_nested_delimiter="__")

    @model_validator(mode="after")
    def compute_compound_fields(self) -> dict:
        self.oidc_conf_url = (
            self.oidc_provider_url.rstrip("/") + "/" + self.oidc_conf_endpoint.lstrip("/")
        )
        self.oidc_token_info_url = (
            self.oidc_provider_url.rstrip("/") + "/" + self.oidc_token_info_endpoint.lstrip("/")
        )
        self.oidc_user_info_url = (
            self.oidc_provider_url.rstrip("/") + "/" + self.oidc_user_info_endpoint.lstrip("/")
        )
        return self


@cache
def get_settings() -> Settings:
    return Settings(_env_file=_settings_file)


def set_settings_file(path: str) -> None:
    global _settings_file
    _settings_file = path
    get_settings.cache_clear()
