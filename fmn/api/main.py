import logging

from fasjson_client import Client as FasjsonClient
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import Settings, get_settings
from ..database import init_async_model
from ..database.model import User
from .auth import Identity, get_identity_optional
from .database import req_db_async_session

log = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
def add_middlewares():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().cors_origins.split(" "),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def init_model():  # pragma: no cover todo
    await init_async_model()


class TrackingRule(BaseModel):
    name: str
    params: list[str] | dict[str, str] | None


class GenerationRule(BaseModel):
    destinations: list[str]
    filters: dict[str, str | list[str] | bool | None]


class Rule(BaseModel):
    name: str
    tracking_rule: TrackingRule
    generation_rules: list[GenerationRule]


def get_fasjson_client(settings: Settings = Depends(get_settings)):
    return FasjsonClient(settings.services.fasjson_url)


@app.get("/")
async def read_root(
    request: Request,
    creds: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
    identity: Identity | None = Depends(get_identity_optional),
):
    result = {
        "Hello": "World",
        "creds": creds,
        "identity": identity,
    }

    return result


@app.get("/users/")
async def get_users(
    db_async_session: AsyncSession = Depends(req_db_async_session),
):  # pragma: no cover todo
    result = await db_async_session.execute(select(User))
    return {"users": result.scalars().all()}


@app.get("/user/{username}/")
async def get_user(
    username, db_async_session: AsyncSession = Depends(req_db_async_session)
):  # pragma: no cover todo
    query = select(User).filter_by(name=username)
    result = await db_async_session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        user = User(name=username)
        db_async_session.add(user)
        await db_async_session.flush()
        await db_async_session.refresh(user)
    return {"user": user}


@app.get("/user/{username}/info")
def get_user_info(
    username, fasjson_client: FasjsonClient = Depends(get_fasjson_client)
):  # pragma: no cover todo
    return fasjson_client.get_user(username=username).result


@app.get("/user/{username}/destinations")
def get_user_destinations(
    username, fasjson_client: FasjsonClient = Depends(get_fasjson_client)
):  # pragma: no cover todo
    user = fasjson_client.get_user(username=username).result
    matrix_nicks = [n for n in user.get("ircnicks", []) if n.startswith("matrix:")]
    irc_nicks = [n for n in user.get("ircnicks", []) if not n.startswith("matrix:")]
    return [
        {"name": "email", "label": "Email", "options": user["emails"]},
        {"name": "irc", "label": "IRC", "options": irc_nicks},
        {"name": "matrix", "label": "Matrix", "options": matrix_nicks},
    ]


@app.get("/user/{username}/rules")
def get_user_rules(username):  # pragma: no cover todo
    return [
        {
            "name": "My Completed Koji Builds",
            "tracking_rule": "artifacts-owned",
            "filters": {
                "severities": [],
                "my_actions": True,
                "topic": "org.fedoraproject.koji.build-complete",
                "applications": ["koji"],
            },
            "destinations": [f"matrix:/{username}"],
        },
        {
            "name": "All Events related to me",
            "tracking_rule": "related-events",
            "filters": {
                "severities": ["warning"],
                "my_actions": True,
                "topic": None,
                "applications": [],
            },
            "destinations": [f"irc:/{username}", f"{username}@tinystage.test"],
        },
    ]


@app.post("/user/{username}/rules")
def create_user_rule(username, rule: Rule):  # pragma: no cover todo
    print("Creating rule:", rule)
    return rule


@app.get("/applications")
def get_applications():  # pragma: no cover todo
    # Read the installed schemas and extract the applications. Return sorted, please :-)
    return [
        "anitya",
        "bodhi",
        "koji",
    ]
