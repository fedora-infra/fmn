from functools import lru_cache

from fasjson_client import Client
from fastapi import FastAPI
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

c = Client("http://fasjson.tinystage.test/fasjson")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/userinfo/{username}")
def get_userinfo(username):
    return c.get_user(username=username).result
