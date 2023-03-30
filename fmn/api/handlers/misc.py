import logging
from importlib import metadata

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...backends import PagureAsyncProxy, get_distgit_proxy
from ...core.constants import ArtifactType
from ...database.migrations.main import alembic_migration
from .. import api_models
from ..database import gen_db_session

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
        artifacts.update(
            (project["fullname"], {"type": project["namespace"], "name": project["name"]})
            for project in await distgit_proxy.get_user_projects(username=user)
            if ArtifactType.has_value(project["namespace"])
        )

    for group in groups:
        artifacts.update(
            (project["fullname"], {"type": project["namespace"], "name": project["name"]})
            for project in await distgit_proxy.get_group_projects(name=group)
            if ArtifactType.has_value(project["namespace"])
        )

    return sorted(artifacts.values(), key=lambda a: (a["name"], a["type"]))


@router.get("/artifacts", response_model=list[api_models.Artifact], tags=["misc"])
async def get_artifacts(name: str, distgit_proxy: PagureAsyncProxy = Depends(get_distgit_proxy)):
    # TODO: handle error 500 in distgit_proxy.get_projects()
    projects = [
        {"type": project["namespace"], "name": project["name"]}
        for project in await distgit_proxy.get_projects(pattern=f"*{name}*")
        if ArtifactType.has_value(project["namespace"])
    ]
    return projects


@router.get("/healthz/live", tags=["healthz"])
async def liveness_check():
    return {"detail": "OK"}


@router.get("/healthz/ready", tags=["healthz"])
async def readiness_check(db_session: AsyncSession = Depends(gen_db_session)):
    try:
        needs_upgrade = await alembic_migration.needs_upgrade(db_session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    if needs_upgrade:
        raise HTTPException(status_code=500, detail="Database schema needs to be upgraded")
    else:
        return {"detail": "OK"}
