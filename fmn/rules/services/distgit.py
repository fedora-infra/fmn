import logging
from itertools import chain
from typing import TYPE_CHECKING

from cashews import cache

from ...backends import PagureAsyncProxy
from ...cache.tracked import TrackedCache
from .utils import handle_http_error, normalize_url

if TYPE_CHECKING:
    from fedora_messaging.message import Message


log = logging.getLogger(__name__)


class DistGitService:
    GROUP_OWNER_LEVELS = ("admin", "commit")

    def __init__(self, url):
        self.url = normalize_url(url)
        self.proxy = PagureAsyncProxy(base_url=url)

    @cache(ttl="6h", prefix="v1")
    @handle_http_error(list)
    async def get_owners(self, artifact_type, artifact_name, user_or_group):
        log.debug(f"Getting {user_or_group} owners of {artifact_type}/{artifact_name}")
        result = await self.proxy.get(f"{artifact_type}/{artifact_name}")
        if user_or_group == "user":
            return result["access_users"]["owner"]
        elif user_or_group == "group":
            return result["access_groups"]["admin"] + result["access_groups"]["commit"]
        else:
            raise ValueError("Argument user_or_group must be either user or group, duh.")

    @cache(ttl="6h", prefix="v1")
    @handle_http_error(list)
    async def get_owned(self, artifact_type, name, user_or_group):
        log.debug(f"Getting owned {artifact_type} by {user_or_group} {name}")
        if user_or_group == "user":
            endpoint = "/projects"
            params = {"namespace": artifact_type, "owner": name, "short": "1"}
        elif user_or_group == "group":
            endpoint = f"/group/{name}"
            params = {"projects": "true"}
        else:
            raise ValueError("Argument user_or_group must be either user or group, duh.")

        return [
            p["name"]
            async for p in self.proxy.get_paginated(
                endpoint, params=params, payload_field="projects"
            )
        ]

    async def invalidate_on_message(self, message: "Message"):
        if message.topic.endswith("pagure.project.user.access.updated"):
            if message.body["new_access"] == "owner":
                await self._on_owner_changed(
                    message.body["project"]["namespace"],
                    message.body["project"]["name"],
                    message.body["new_user"],
                    "user",
                )
        elif message.topic.endswith("pagure.project.user.added"):
            if message.body["new_user"] in message.body["project"]["access_users"]["owner"]:
                await self._on_owner_changed(
                    message.body["project"]["namespace"],
                    message.body["project"]["name"],
                    message.body["new_user"],
                    "user",
                )
        # On user.removed, the Pagure message does not tell us which access level they had.
        # Do nothing.
        elif message.topic.endswith("pagure.project.group.access.updated"):
            if message.body["new_access"] in self.GROUP_OWNER_LEVELS:
                await self._on_owner_changed(
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
                await self._on_owner_changed(
                    message.body["project"]["namespace"],
                    message.body["project"]["name"],
                    message.body["new_group"],
                    "group",
                )
        elif message.topic.endswith("pagure.project.group.removed"):
            if message.body["access"] in self.GROUP_OWNER_LEVELS:
                for group_name in message.body["removed_groups"]:
                    await self._on_owner_changed(
                        message.body["project"]["namespace"],
                        message.body["project"]["name"],
                        group_name,
                        "group",
                    )

    async def _on_owner_changed(self, namespace, project_name, name, user_or_group):
        # Don't use the cache.invalidate() decorator as it will invalidate the cache *after* the
        # function has been run, and we want to refresh it here.
        await cache.invalidate_func(
            self.get_owners,
            {
                "artifact_type": namespace,
                "artifact_name": project_name,
                "user_or_group": user_or_group,
            },
        )
        await cache.invalidate_func(
            self.get_owned,
            {
                "artifact_type": namespace,
                "name": name,
                "user_or_group": user_or_group,
            },
        )
        # Now rebuild the cache to ease the work on the next incoming message
        await self.get_owners(namespace, project_name, user_or_group)
        await self.get_owned(namespace, name, user_or_group)
        tracked_cache = TrackedCache()
        await tracked_cache.invalidate()
        # We can't rebuild the tracked cache here because we don't have access to the DB and
        # Requester objects.
