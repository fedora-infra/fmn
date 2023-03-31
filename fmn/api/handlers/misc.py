import logging
from importlib import metadata
from itertools import chain

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


@router.get("/artifacts", response_model=list[api_models.Artifact], tags=["misc"])
async def get_artifacts(
    names: list[str] = Query(default=[]),
    users: list[str] = Query(default=[]),
    groups: list[str] = Query(default=[]),
    distgit_proxy: PagureAsyncProxy = Depends(get_distgit_proxy),
):
    """This handler queries artifacts from Pagure

    Proxying Pagure queries lets the API cache results to reduce load on the
    backend service.

    :param names: Name patterns of artifacts which should be returned

    :param users: Names of users whose artifacts should be returned

    :param groups: Names of groups whose artifacts should be returned
    """
    backend_coroutines = chain(
        (distgit_proxy.get_projects(pattern=name_pattern) for name_pattern in names),
        (distgit_proxy.get_user_projects(username=user) for user in users),
        (distgit_proxy.get_group_projects(name=group) for group in groups),
    )

    backend_results = chain.from_iterable([await coroutine for coroutine in backend_coroutines])

    artifacts = sorted(
        {
            (project["name"], project["namespace"])
            for project in backend_results
            if ArtifactType.has_value(project["namespace"])
        }
    )

    return [{"type": artifact[1], "name": artifact[0]} for artifact in artifacts]


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
