# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from functools import cache
from importlib import metadata
from itertools import chain

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy_helpers import DatabaseStatus

from ...backends import PagureAsyncProxy, get_distgit_proxy
from ...core.constants import ArtifactType
from .. import api_models
from ..database import gen_db_manager

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/applications", response_model=list[str], tags=["misc"])
@cache
def get_applications():
    entrypoints = metadata.entry_points().select(group="fedora.messages")

    # dictionary of normalized, lower case application name to pristine name
    applications = {}

    for ep in entrypoints:
        msg_cls = ep.load()
        try:
            app_name = msg_cls.app_name.fget(None)
            if app_name is None:
                raise ValueError("app_name is None")
        except Exception:
            # Sometimes the schema hasn't set the app_name. Fallback on the entry point name.
            app_name = ep.name.partition(".")[0]

        app_name_lower = app_name.lower()
        if (
            # we will always have the base message in there, so lets discard that
            app_name_lower != "base"
            # and prefer variations of names with more leading capital characters
            and (app_name_lower not in applications or app_name < applications[app_name_lower])
        ):
            applications[app_name_lower] = app_name

    # return list sorted by lowercase name, but with case left intact
    return [item[1] for item in sorted(applications.items(), key=lambda item: item[0])]


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
async def readiness_check(db_manager=Depends(gen_db_manager)):
    try:
        status = await db_manager.get_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Can't get the database status: {e}") from e
    if status is DatabaseStatus.NO_INFO:
        raise HTTPException(status_code=500, detail="Can't connect to the database")
    if status is DatabaseStatus.UPGRADE_AVAILABLE:
        raise HTTPException(status_code=500, detail="Database schema needs to be upgraded")
    return {"detail": "OK"}
