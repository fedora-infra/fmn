from pydantic import BaseSettings


class Settings(BaseSettings):
    cors_origins: str = "https://notifications.fedoraproject.org"

    class Config:
        env_file = "fmn.cfg"
