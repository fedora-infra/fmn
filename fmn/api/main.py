from functools import lru_cache
from typing import Union

from fasjson_client import Client as FasjsonClient
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


class Rule(BaseModel):
    name: str
    tracking_rule: str
    destinations: list[str]
    filters: dict[str, Union[str, bool, None]]


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
        {"name": "email", "label": "Email", "options": user["emails"]},
        {"name": "irc", "label": "IRC", "options": irc_nicks},
        {"name": "matrix", "label": "Matrix", "options": matrix_nicks},
    ]


@app.get("/user/{username}/rules")
def get_user_rules(username):  # pragma: no cover
    return [
        {
            "name": "My Completed Koji Builds",
            "tracking_rule": "artifact-owned",
            "filters": {
                "severity": None,
                "my_actions": True,
                "topic": "org.fedoraproject.koji.build-complete",
                "application": "koji",
            },
            "destinations": [f"matrix:/{username}"],
        },
        {
            "name": "All Events related to me",
            "tracking_rule": "related-events",
            "filters": {
                "severity": "warning",
                "my_actions": True,
                "topic": None,
                "application": None,
            },
            "destinations": [f"irc:/{username}", f"{username}@tinystage.test"],
        },
    ]


@app.post("/user/{username}/rules")
def create_user_rule(username, rule: Rule):  # pragma: no cover
    print("Creating rule:", rule)
    return rule


@app.get("/applications")
def get_applications():  # pragma: no cover
    # Read the installed schemas and extract the applications. Return sorted, please :-)
    return [
        "anitya",
        "bodhi",
        "koji",
    ]
