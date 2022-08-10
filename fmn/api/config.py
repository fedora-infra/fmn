from pydantic import BaseSettings


class Settings(BaseSettings):
    cors_origins: str = "https://notifications.fedoraproject.org"
    fasjson_url: str = "https://fasjson.fedoraproject.org"

    class Config:
        env_file = "fmn.cfg"
