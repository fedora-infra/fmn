import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from fmn.api import api_models
from fmn.api.auth import Identity, get_identity
from fmn.api.distgit import DistGitClient, get_distgit_client
from fmn.core.constants import ArtifactType
from fmn.database.model import User
from fmn.rules.notification import Notification
from fmn.rules.requester import Requester

from .utils import db_rule_from_api_rule, gen_requester, get_last_messages

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


# Note: this function can't be async.
# The message handling by the rules is synchronous because it is run by the consumer in a thread
# that fedora-messaging provides (via Twisted) and we don't dare mix Twisted async with asyncio.
@router.post("/rule-preview", response_model=list[Notification], tags=["users/rules"])
def preview_rule(
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

    log.debug("Previewing rule:", rule)
    user = User(name=identity.name)
    rule_db = db_rule_from_api_rule(rule, user)
    rule_db.id = 0
    notifs = []
    # TODO make the delta a setting
    # TODO: this takes ridiculously long.
    for message in get_last_messages(1):
        log.debug(f"Processing message: {message.body}")
        for notif in rule_db.handle(message, requester):
            notifs.append(notif)
    return notifs
