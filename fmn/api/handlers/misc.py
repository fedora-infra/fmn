import logging

from fastapi import APIRouter, Depends, Query

from fmn.api import api_models
from fmn.core.constants import ArtifactType

from ..distgit import DistGitClient, get_distgit_client

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/applications", response_model=list[str], tags=["misc"])
def get_applications():
    # TODO: Read the installed schemas and extract the applications. Return sorted, please :-)
    return [
        "anitya",
        "bodhi",
        "koji",
    ]


@router.get("/artifacts/owned", response_model=list[dict[str, str]], tags=["misc"])
def get_owned_artifacts(
    users: list[str] = Query(default=[]), groups: list[str] = Query(default=[])
):
    # TODO: Get artifacts owned by a user or a group

    artifacts = []
    artifact_names = []

    def _add_artifact(a):
        if a["name"] in artifact_names:
            return
        artifacts.append(a)
        artifact_names.append(a["name"])

    for username in users or []:
        # Add artifacts owned by the user to the list
        _add_artifact({"type": "rpm", "name": "foobar-user-owned"})
    for groupname in groups or []:
        # Add artifacts owned by the user to the list
        _add_artifact({"type": "rpm", "name": "foobar-group-owned"})
    artifacts.sort(key=lambda a: a["name"])
    return artifacts


@router.get("/artifacts", response_model=list[api_models.ArtifactOptionsGroup], tags=["misc"])
async def get_artifacts(
    name: str, distgit_client: DistGitClient = Depends(get_distgit_client)
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
    projects = await distgit_client.get_projects(pattern=name)
    for project in projects:
        for index, namespace in enumerate(namespaces):
            if project["namespace"] == namespace:
                artifacts[index]["options"].append(
                    {
                        "label": project["name"],
                        "value": {"type": namespace, "name": project["name"]},
                    }
                )
    return artifacts
