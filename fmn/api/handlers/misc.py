import logging
from importlib import metadata

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...backends import PagureAsyncProxy
from ...core.constants import ArtifactType
from ...database.migrations.main import alembic_migration
from ...database.model import User
from ...rules.notification import Notification
from ...rules.requester import Requester
from .. import api_models
from ..auth import Identity, get_identity
from ..database import gen_db_session
from ..distgit import get_distgit_proxy
from .utils import db_rule_from_api_rule, gen_requester, get_last_messages

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/applications", response_model=list[str], tags=["misc"])
def get_applications():
    entrypoints = metadata.entry_points().select(group="fedora.messages")
    applications = set()
    for ep in entrypoints:
        msg_cls = ep.load()
        try:
            app_name = msg_cls.app_name.fget(None)
            if app_name is None:
                raise ValueError("app_name is None")
        except Exception:
            # Sometimes the schema hasn't set the app_name. Fallback on the entry point name.
            app_name = ep.name.partition(".")[0]
        applications.add(app_name)

    # we will always have the base message in there, so lets discard that
    applications.discard("base")
    applications = list(applications)
    applications.sort(key=lambda name: name.lower())

    return applications


@router.get("/artifacts/owned", response_model=list[dict[str, str]], tags=["misc"])
async def get_owned_artifacts(
    users: list[str] = Query(default=[]),
    groups: list[str] = Query(default=[]),
    distgit_proxy: PagureAsyncProxy = Depends(get_distgit_proxy),
):
    artifacts = {}

    for user in users:
        for project in await distgit_proxy.get_user_projects(username=user):
            artifacts[project["fullname"]] = {"type": project["namespace"], "name": project["name"]}

    for group in groups:
        for project in await distgit_proxy.get_group_projects(name=group):
            artifacts[project["fullname"]] = {"type": project["namespace"], "name": project["name"]}

    return sorted(artifacts.values(), key=lambda a: (a["name"], a["type"]))


@router.get("/artifacts", response_model=list[api_models.ArtifactOptionsGroup], tags=["misc"])
async def get_artifacts(
    name: str, distgit_proxy: PagureAsyncProxy = Depends(get_distgit_proxy)
):  # pragma: no cover todo
    artifacts = [
        {
            "label": "RPMs",
            "options": [],
        },
        {
            "label": "Containers",
            "options": [],
        },
        {
            "label": "Modules",
            "options": [],
        },
        {
            "label": "Flatpaks",
            "options": [],
        },
    ]
    namespaces = [at.value for at in ArtifactType]
    # TODO: handle error 500 in distgit_proxy.get_projects()
    for project in await distgit_proxy.get_projects(pattern=f"*{name}*"):
        for index, namespace in enumerate(namespaces):
            if project["namespace"] == namespace:
                artifacts[index]["options"].append(
                    {
                        "label": project["name"],
                        "value": {"type": namespace, "name": project["name"]},
                    }
                )
    return artifacts


@router.post("/rule-preview", response_model=list[Notification], tags=["users/rules"])
async def preview_rule(
    rule: api_models.RulePreview,
    identity: Identity = Depends(get_identity),
    requester: Requester = Depends(gen_requester),
):
    if identity.name is None:
        raise HTTPException(status_code=403, detail="You need to be logged in")

    # Make sure each GenerationRule has one destination, otherwise no notifications will
    # be produced (or too many).
    for gr in rule.generation_rules:
        gr.destinations = [api_models.Destination(protocol="preview", address="preview")]

    log.debug("Previewing rule: %s", rule)
    user = User(name=identity.name)
    rule_db = db_rule_from_api_rule(rule, user)
    rule_db.id = 0
    notifs = []
    # TODO make the delta a setting
    # TODO: this takes ridiculously long.
    async for message in get_last_messages(1):
        log.debug("Processing message: %s", message.body)
        async for notif in rule_db.handle(message, requester):
            notifs.append(notif)
    return notifs


@router.get("/healthz/live", tags=["healthz"])
async def liveness_check():
    return {"detail": "OK"}


@router.get("/healthz/ready", tags=["healthz"])
async def readiness_check(db_session: AsyncSession = Depends(gen_db_session)):
    try:
        needs_upgrade = await alembic_migration.needs_upgrade(db_session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if needs_upgrade:
        raise HTTPException(status_code=500, detail="Database schema needs to be upgraded")
    else:
        return {"detail": "OK"}
