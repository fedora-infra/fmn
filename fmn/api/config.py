from functools import cache

from pydantic import BaseSettings

settings_file = None  # will be set from CLI


class Settings(BaseSettings):
    cors_origins: str = "https://notifications.fedoraproject.org"
    fasjson_url: str = "https://fasjson.fedoraproject.org"

    class Config:
        env_file = "fmn.cfg"


@cache
def get_settings() -> Settings:
    return Settings(_env_file=settings_file)
