from functools import lru_cache

from fasjson_client import Client as FasjsonClient
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings

app = FastAPI()


@lru_cache()
def get_settings():
    return Settings()


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins.split(" "),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_fasjson_client(settings: Settings = Depends(get_settings)):
    return FasjsonClient(settings.fasjson_url)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/userinfo/{username}")
def get_userinfo(username, fasjson_client: FasjsonClient = Depends(get_fasjson_client)):
    return fasjson_client.get_user(username=username).result
