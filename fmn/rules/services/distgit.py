import logging
from itertools import chain
from typing import TYPE_CHECKING

import requests

from ..cache import cache

if TYPE_CHECKING:
    from fedora_messaging.message import Message


log = logging.getLogger(__name__)


class DistGitService:
    GROUP_OWNER_LEVELS = ("admin", "commit")

    def __init__(self, url):
        self.url = url
        self.req = requests.Session()

    def _get(self, url, params=None):
        result = self.req.get(url=url, params=params)
        result.raise_for_status()
        return result.json()

    def _all_values(self, key, url, params=None):
        params["page"] = "1"
        response = self._get(url, params)
        objects = response.get(key)
        while response.get("pagination", {}).get("next"):
            response = self._get(response["pagination"]["next"])
            objects.extend(response.get(key))
        return objects

    @cache.cache_on_arguments()
    def get_owners(self, artifact_type, artifact_name, user_or_group):
        # cache this for a reasonable time
        url = f"{self.url}api/0/{artifact_type}/{artifact_name}"
        response = self._get(url)
        if user_or_group == "user":
            return response["access_users"]["owner"]
        elif user_or_group == "group":
            return response["access_groups"]["admin"] + response["access_groups"]["commit"]
        else:
            raise ValueError("Argument user_or_group must be either user or group, duh.")

    @cache.cache_on_arguments()
    def get_owned(self, artifact_type, name, user_or_group):
        # cache this for a reasonable time
        if artifact_type == "package":
            artifact_type = "rpms"
        if user_or_group == "user":
            projects = self._all_values(
                "projects",
                f"{self.url}api/0/projects",
                {"namespace": artifact_type, "owner": name, "short": "1"},
            )
        elif user_or_group == "group":
            projects = self._all_values(
                "projects",
                f"{self.url}api/0/projects",
                {"namespace": artifact_type, "username": f"@{name}", "short": "1"},
            )
        else:
            raise ValueError("Argument user_or_group must be either user or group, duh.")
        return [p["name"] for p in projects]

    def invalidate_on_message(self, message: "Message"):
        if message.topic.endswith("pagure.project.user.access.updated"):
            if message.body["new_access"] == "owner":
                self._on_owner_changed(
                    message.body["project"]["namespace"],
                    message.body["project"]["name"],
                    message.body["new_user"],
                    "user",
                )
        elif message.topic.endswith("pagure.project.user.added"):
            if message.body["new_user"] in message.body["project"]["access_users"]["owner"]:
                self._on_owner_changed(
                    message.body["project"]["namespace"],
                    message.body["project"]["name"],
                    message.body["new_user"],
                    "user",
                )
        # On user.removed, the Pagure message does not tell us which access level they had.
        # Do nothing.
        elif message.topic.endswith("pagure.project.group.access.updated"):
            if message.body["new_access"] in self.GROUP_OWNER_LEVELS:
                self._on_owner_changed(
                    message.body["project"]["namespace"],
                    message.body["project"]["name"],
                    message.body["new_group"],
                    "group",
                )
        elif message.topic.endswith("pagure.project.group.added"):
            owner_accesses = [
                message.body["project"]["access_groups"][level] for level in self.GROUP_OWNER_LEVELS
            ]
            owners = list(chain(*owner_accesses))
            if message.body["new_group"] in owners:
                self._on_owner_changed(
                    message.body["project"]["namespace"],
                    message.body["project"]["name"],
                    message.body["new_group"],
                    "group",
                )
        elif message.topic.endswith("pagure.project.group.removed"):
            if message.body["access"] in self.GROUP_OWNER_LEVELS:
                self._on_owner_changed(
                    message.body["project"]["namespace"],
                    message.body["project"]["name"],
                    message.body["new_group"],
                    "group",
                )

    def _on_owner_changed(self, namespace, project_name, name, user_or_group):
        self.get_owners.refresh(self, namespace, project_name, user_or_group)
        self.get_owned.refresh(self, namespace, name, user_or_group)
        cache.invalidate_tracked()
