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


@app.get("/user/{username}/info")
def get_user_info(
    username, fasjson_client: FasjsonClient = Depends(get_fasjson_client)
):  # pragma: no cover
    return fasjson_client.get_user(username=username).result


@app.get("/user/{username}/destinations")
def get_user_destinations(
    username, fasjson_client: FasjsonClient = Depends(get_fasjson_client)
):  # pragma: no cover
    user = fasjson_client.get_user(username=username).result
    matrix_nicks = [n for n in user.get("ircnicks", []) if n.startswith("matrix:")]
    irc_nicks = [n for n in user.get("ircnicks", []) if not n.startswith("matrix:")]
    return [
        {"name": "email", "title": "Email", "values": user["emails"]},
        {"name": "irc", "title": "IRC", "values": irc_nicks},
        {"name": "matrix", "title": "Matrix", "values": matrix_nicks},
    ]


@app.get("/rules")
def get_rules():  # pragma: no cover
    return [
        {"name": "artifact-owned", "title": "Artifacts owned by me"},
        {"name": "artifact-group-owned", "title": "Artifacts owned by one of my groups"},
        {"name": "artifact-followed", "title": "Artifacts I follow"},
        {"name": "related-events", "title": "Events referring to me"},
        {"name": "user-followed", "title": "Users I follow"},
    ]


@app.get("/filters")
def get_filters():  # pragma: no cover
    # Read the installed schemas and extract the applications. Return sorted, please :-)
    available_apps = [
        "anitya",
        "bodhi",
        "koji",
    ]
    return [
        {"name": "application", "title": "Application", "choices": available_apps},
        {"name": "severity", "title": "Severity", "choices": ["debug", "info", "warning", "error"]},
        {"name": "my-actions", "title": "My Actions"},
        {"name": "topic", "title": "Topic", "str_arg": True},
    ]
