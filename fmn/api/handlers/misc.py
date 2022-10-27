import logging

from fastapi import APIRouter, Query

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


@router.get("/artifacts", response_model=list[str], tags=["misc"])
def get_artifacts(type: str, name: str):  # pragma: no cover todo
    # TODO: Get artifacts

    artifacts = []

    artifacts.append(f"foobar-{name}")
    artifacts.append(f"foo-{name}")
    artifacts.append(f"bar-{name}")

    return artifacts
