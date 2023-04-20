# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
import bisect
import logging
import re
from enum import IntFlag, auto
from functools import cache as ft_cache
from functools import cached_property as ft_cached_property
from itertools import chain
from typing import TYPE_CHECKING, Any

from cashews import cache
from httpx import URL, QueryParams

from ..cache.util import cache_ttl, get_pattern_for_cached_calls
from ..core.config import get_settings
from .base import APIClient, NextPageParams, handle_http_error

if TYPE_CHECKING:
    from fedora_messaging.message import Message
    from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)


class PagureRole(IntFlag):
    OWNER = auto()
    ADMIN = auto()
    COMMIT = auto()
    COLLABORATOR = auto()
    TICKET = auto()

    USER_ROLES_MAINTAINER = OWNER | ADMIN | COMMIT | COLLABORATOR
    USER_ROLES = USER_ROLES_MAINTAINER | TICKET
    GROUP_ROLES_MAINTAINER = ADMIN | COMMIT | COLLABORATOR
    GROUP_ROLES = GROUP_ROLES_MAINTAINER | TICKET


# Python < 3.11 doesn’t allow iterating over combined flag values
PagureRole.USER_ROLES_MAINTAINER_SET = {
    role for role in PagureRole if role.bit_count() == 1 and role & PagureRole.USER_ROLES_MAINTAINER
}
PagureRole.USER_ROLES_SET = {
    role for role in PagureRole if role.bit_count() == 1 and role & PagureRole.USER_ROLES
}
PagureRole.GROUP_ROLES_MAINTAINER_SET = {
    role
    for role in PagureRole
    if role.bit_count() == 1 and role & PagureRole.GROUP_ROLES_MAINTAINER
}
PagureRole.GROUP_ROLES_SET = {
    role for role in PagureRole if role.bit_count() == 1 and role & PagureRole.GROUP_ROLES
}


class PagureAsyncProxy(APIClient):
    """Proxy for the FASJSON API endpoints used in FMN"""

    API_VERSION = "0"

    PROJECT_TOPIC_RE = re.compile(
        r"pagure\.project\.(?P<usergroup>user|group)\.(?P<action>access\.updated|added|removed)$"
    )

    @ft_cached_property
    def api_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/api/{self.API_VERSION}"

    def determine_next_page_params(self, url: str, params: dict, result: dict) -> NextPageParams:
        next_url = result.get("pagination", {}).get("next")
        if next_url:
            parsed_url = URL(next_url)
            parsed_query_params = QueryParams(parsed_url.query)
            next_params = {**params, **parsed_query_params}
            next_url = str(parsed_url.copy_with(query=None))

            return next_url, next_params

        return None, None

    @handle_http_error(list)
    @cache(ttl=cache_ttl("pagure"), prefix="v1")
    async def get_projects(
        self,
        *,
        namespace: str | None = None,
        pattern: str | None = None,
        username: str | None = None,
        owner: str | None = None,
        short: bool = True,
        fork: bool = False,
    ) -> list[dict[str, Any]]:
        params = {"short": short, "fork": fork}
        if namespace:
            params["namespace"] = namespace
        if pattern:
            params["pattern"] = pattern
        if username:
            params["username"] = username
        if owner:
            params["owner"] = owner

        return [
            project
            async for project in self.get_paginated(
                "/projects", params=params, payload_field="projects"
            )
        ]

    @handle_http_error(list)
    @cache(ttl=cache_ttl("pagure"), prefix="v1")
    async def get_user_projects(self, *, username: str) -> list[dict[str, Any]]:
        return [
            p
            for p in await self.get_projects(username=username, short=False)
            if any(
                username in p.get("access_users", {}).get(role.name.lower(), [])
                for role in PagureRole.USER_ROLES_MAINTAINER_SET
            )
        ]

    @handle_http_error(list)
    @cache(ttl=cache_ttl("pagure"), prefix="v1")
    async def get_project_users(
        self, *, project_path: str, roles: PagureRole = PagureRole.USER_ROLES_MAINTAINER
    ) -> list[str]:
        project = await self.get(project_path)
        access_users = project.get("access_users", {})
        usernames = {
            username
            for role in PagureRole
            for username in access_users.get(role.name.lower(), ())
            if role in roles
        }
        return sorted(usernames)

    @handle_http_error(list)
    @cache(ttl=cache_ttl("pagure"), prefix="v1")
    async def get_project_groups(
        self, *, project_path: str, roles: PagureRole = PagureRole.GROUP_ROLES_MAINTAINER
    ) -> list[str]:
        project = await self.get(project_path)
        access_groups = project.get("access_groups", {})
        groupnames = {
            groupname
            for role in PagureRole
            for groupname in access_groups.get(role.name.lower(), ())
            if role in roles
        }
        return sorted(groupnames)

    @handle_http_error(list)
    @cache(ttl=cache_ttl("pagure"), prefix="v1")
    async def get_group_projects(
        self, *, name: str, acl: PagureRole | None = None
    ) -> list[dict[str, Any]]:
        if not acl:
            params_seq = ({"projects": True},)
        else:
            params_seq = [
                {"projects": True, "acl": role.name.lower()}
                for role in PagureRole.GROUP_ROLES_SET
                if role & acl
            ]

        seen_fullnames = set()
        sorted_projects = []
        for params in params_seq:
            async for project in self.get_paginated(
                f"/group/{name}", params=params, payload_field="projects"
            ):
                if (fullname := project["fullname"]) in seen_fullnames:
                    continue
                seen_fullnames.add(fullname)
                bisect.insort(sorted_projects, project, key=lambda p: p["fullname"])
        return sorted_projects

    async def invalidate_on_message(self, message: "Message", db: "AsyncSession") -> None:
        topic = message.topic
        topic_match = self.PROJECT_TOPIC_RE.search(topic)
        if not topic_match:
            # Bail out early
            log.debug("Skipping message with topic %s", topic)
            return

        # Quick access
        body = message.body
        usergroup = topic_match.group("usergroup")
        action = topic_match.group("action")

        if not (msg_project := body.get("project")):
            log.warning("No project info found when processing message")
            return

        if not (fullname := msg_project.get("fullname")):
            log.warning("No full name found for affected project when processing message")
            return

        if not (full_url := msg_project.get("full_url")):
            log.warning("No URL found for affected project when processing message")
            return

        if not full_url.startswith(self.base_url_with_trailing_slash):
            # Different Pagure instance
            log.debug("Skipping message for different Pagure instance %s", full_url)
            return

        # These keys describe cache entries to be deleted
        del_keys = []

        # Identify cache entries to be invalidated and create tasks for their deletion

        if usergroup == "user":
            # Messages about changes to project users
            if action == "removed":
                user = body.get("removed_user")
            else:
                user = body.get("new_user")

            if not user:
                log.warning("No affected user found when processing message")
                return

            del_keys = [
                key
                for pattern in chain(
                    get_pattern_for_cached_calls(
                        self.get_project_users, self=self, project_path=fullname
                    ),
                    get_pattern_for_cached_calls(
                        self.get_projects, self=self, username=None, owner=None
                    ),
                    get_pattern_for_cached_calls(self.get_projects, self=self, username=user),
                    get_pattern_for_cached_calls(self.get_projects, self=self, owner=user),
                )
                async for key, _ in cache.get_match(pattern)
            ]
        else:  # usergroup == "group"
            # Messages about changes to project groups
            if action == "removed":
                # Messages with topic "project.group.removed" can send a list of groups, but the
                # code in Pagure sending them guarantees it can be at most one 🤔.
                group = body.get("removed_groups", [None])[0]
            else:
                group = body.get("new_group")

            if not group:
                log.warning("No affected group found when processing message")
                return

            del_keys = [
                key
                for pattern in chain(
                    get_pattern_for_cached_calls(
                        self.get_project_groups, self=self, project_path=fullname
                    ),
                    get_pattern_for_cached_calls(self.get_group_projects, self=self, name=group),
                )
                async for key, _ in cache.get_match(pattern)
            ]

        # Delete the things in parallel
        del_tasks = [asyncio.create_task(cache.delete(key)) for key in del_keys]
        del_results = await asyncio.gather(*del_tasks, return_exceptions=True)

        # Follow-up care

        if exceptions_in_results := [
            result for result in del_results if isinstance(result, Exception)
        ]:
            log.warning(
                "Deleting %d cache entries yielded %d exception(s):",
                len(del_results),
                len(exceptions_in_results),
            )
            for exc in exceptions_in_results:
                log.warning("\t%r", exc)


@ft_cache
def get_distgit_proxy() -> PagureAsyncProxy:
    return PagureAsyncProxy(get_settings().services.distgit_url)
