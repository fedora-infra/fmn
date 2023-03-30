# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from typing import TYPE_CHECKING

from ..backends import PagureRole
from ..core.constants import ArtifactType
from .requester import Requester

if TYPE_CHECKING:
    from fedora_messaging.message import Message


log = logging.getLogger(__name__)


class TrackingRule:
    # This should be the name of the Tracking rule in the Database
    name: str | None = None

    def __init__(self, requester: Requester, params, owner):
        self._requester = requester
        self._params = params
        self._owner = owner

    async def matches(self, message: "Message"):
        raise NotImplementedError

    async def prime_cache(self, cache):
        raise NotImplementedError


class ArtifactsOwned(TrackingRule):
    name = "artifacts-owned"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usernames = set(self._params)

    async def matches(self, message):
        for artifact_type in ArtifactType:
            for artifact in getattr(message, artifact_type.name):
                owners = await self._requester.distgit.get_project_users(
                    project_path=f"{artifact_type.value}/{artifact}"
                )
                if self.usernames & set(owners):
                    return True
        return False

    async def prime_cache(self, cache):
        for username in self.usernames:
            owned = await self._requester.distgit.get_user_projects(username=username)
            for artifact_type in ArtifactType:
                getattr(cache, artifact_type.name).update(
                    p["name"] for p in owned if p["namespace"] == artifact_type.value
                )


class ArtifactsGroupOwned(TrackingRule):
    name = "artifacts-group-owned"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = set(self._params)

    async def matches(self, message):
        for artifact_type in ArtifactType:
            for artifact in getattr(message, artifact_type.name):
                owners = await self._requester.distgit.get_project_groups(
                    project_path=f"{artifact_type.value}/{artifact}"
                )
                if self.groups & set(owners):
                    return True
        return False

    async def prime_cache(self, cache):
        for group in self.groups:
            owned = await self._requester.distgit.get_group_projects(
                name=group, acl=PagureRole.GROUP_ROLES_MAINTAINER
            )
            for role in PagureRole.GROUP_ROLES_MAINTAINER_SET:
                for artifact_type in ArtifactType:
                    getattr(cache, artifact_type.name).update(
                        p["fullname"]
                        for p in owned
                        if p["namespace"] == artifact_type.value
                        and group in p["access_groups"].get(role.name.lower(), ())
                    )


class ArtifactsFollowed(TrackingRule):
    name = "artifacts-followed"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.followed = {
            atype.name: {p["name"] for p in self._params if p["type"] == atype.value}
            for atype in ArtifactType
        }
        # → packages: {"pkg1", "pkg2", "pkg3"}

    async def matches(self, message):
        for msg_attr, followed in self.followed.items():
            if not followed:
                continue
            if set(followed).intersection(set(getattr(message, msg_attr))):
                return True
        return False

    async def prime_cache(self, cache):
        for msg_attr, followed in self.followed.items():
            if not followed:
                continue
            getattr(cache, msg_attr).update(followed)


class RelatedEvents(TrackingRule):
    name = "related-events"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def matches(self, message):
        return self._owner in message.usernames

    async def prime_cache(self, cache):
        cache.usernames.add(self._owner)


class UsersFollowed(TrackingRule):
    name = "users-followed"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.followed = set(self._params)

    async def matches(self, message):
        return message.agent_name in self.followed

    async def prime_cache(self, cache):
        cache.agent_name.update(self.followed)
