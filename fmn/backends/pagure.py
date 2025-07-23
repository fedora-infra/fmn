# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import bisect
import logging
import re
from enum import IntFlag, auto
from functools import cache as ft_cache
from functools import cached_property as ft_cached_property
from typing import TYPE_CHECKING, Any

import sqlalchemy as sa
from cashews import cache
from httpx import URL, QueryParams
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..cache.util import cache_ttl
from ..core.config import Settings, get_settings
from .base import APIClient, NextPageParams, handle_http_error
from .pagure_models import PagureGroup, PagureUserGroup, Project, ProjectGroup, ProjectUser, User

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


class PagureAsyncProxy(APIClient):
    """Proxy for the Pagure API endpoints used in FMN.

    TODO: Drop this implementation once the direct-db implementation has proven itself.
    (in a few months? let's say sept 2025)
    """

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

    @cache(
        ttl=cache_ttl("pagure"),
        prefix="v1",
        tags=[
            "pagure:get_projects:username={username}:owner={owner}",
            "pagure:get_projects:username={username}",
            "pagure:get_projects:owner={owner}",
        ],
    )
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

    @cache(ttl=cache_ttl("pagure"), prefix="v1")
    async def get_user_projects(self, *, username: str) -> list[dict[str, Any]]:
        return [
            p
            for p in await self.get_projects(username=username, short=False)
            if any(
                username in p.get("access_users", {}).get(role.name.lower(), [])
                for role in PagureRole.USER_ROLES_MAINTAINER
            )
        ]

    @handle_http_error(list)
    @cache(
        ttl=cache_ttl("pagure"),
        prefix="v1",
        tags=["pagure:get_project_users:project_path={project_path}"],
    )
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
    @cache(
        ttl=cache_ttl("pagure"),
        prefix="v1",
        tags=["pagure:get_project_groups:project_path={project_path}"],
    )
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

    @cache(ttl=cache_ttl("pagure"), prefix="v1", tags=["pagure:get_group_projects:name={name}"])
    async def get_group_projects(
        self, *, name: str, acl: PagureRole | None = None
    ) -> list[dict[str, Any]]:
        if not acl:
            params_seq = ({"projects": True},)
        else:
            params_seq = [
                {"projects": True, "acl": role.name.lower()}
                for role in PagureRole.GROUP_ROLES
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

            del_tags = [
                f"pagure:get_project_users:project_path={fullname}",
                "pagure:get_projects:username=:owner=",
                f"pagure:get_projects:username={user}",
                f"pagure:get_projects:owner={user}",
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

            del_tags = [
                f"pagure:get_project_groups:project_path={fullname}",
                f"pagure:get_group_projects:name={group}",
            ]

        try:
            await cache.delete_tags(*del_tags)
        except Exception as exc:
            log.warning("Deleting cache entries yielded an exception: %s", exc)


class PagureDBProxy:
    """Proxy for the Pagure DB queries used in FMN"""

    PROJECT_TOPIC_RE = re.compile(
        r"pagure\.project\.(?P<usergroup>user|group)\.(?P<action>access\.updated|added|removed)$"
    )

    def __init__(self, engine: AsyncEngine, base_url: str | None = None):
        self._engine = engine
        self.Session = async_sessionmaker(self._engine, expire_on_commit=False)
        self.base_url = base_url.rstrip("/") + "/"

    async def start(self):
        pass

    async def stop(self):
        await self._engine.dispose()

    @cache(
        ttl=cache_ttl("pagure"),
        prefix="v1",
        tags=[
            "pagure:get_projects:maintainer={maintainer}:owner={owner}",
            "pagure:get_projects:maintainer={maintainer}",
            "pagure:get_projects:owner={owner}",
        ],
    )
    async def get_projects(
        self,
        *,
        namespace: str | None = None,
        pattern: str | None = None,
        maintainer: str | None = None,
        owner: str | None = None,
        fork: bool = False,
    ) -> list[dict[str, Any]]:
        filters = [Project.is_fork == fork]
        if namespace:
            filters.append(Project.namespace == namespace)
        if pattern:
            if "*" in pattern:
                filters.append(Project.name.ilike(pattern.replace("*", "%")))
            else:
                filters.append(Project.name == pattern)
        query = sa.select(Project.id).where(*filters)
        if owner:
            query = query.join(User, User.id == Project.user_id).where(User.user == owner)
        if maintainer:
            # User created the project
            query = query.join(User, User.id == Project.user_id).where(User.user == maintainer)
            permissions = [r.name.lower() for r in PagureRole.USER_ROLES_MAINTAINER]
            # User got admin or commit right
            sub_q2 = (
                sa.select(Project.id)
                .join(ProjectUser)
                .join(User, ProjectUser.user_id == User.id)
                .where(User.user == maintainer, ProjectUser.access.in_(permissions), *filters)
            )
            # User created a group that has admin or commit right
            sub_q3 = (
                sa.select(Project.id)
                .join(ProjectGroup, ProjectGroup.project_id == Project.id)
                .join(PagureGroup, PagureGroup.id == ProjectGroup.group_id)
                .join(User, PagureGroup.user_id == User.id)
                .where(User.user == maintainer, ProjectGroup.access.in_(permissions), *filters)
            )
            # User is part of a group that has admin or commit right
            sub_q4 = (
                sa.select(Project.id)
                .join(ProjectGroup, ProjectGroup.project_id == Project.id)
                .join(PagureGroup, PagureGroup.id == ProjectGroup.group_id)
                .join(PagureUserGroup, PagureUserGroup.group_id == PagureGroup.id)
                .join(User, PagureUserGroup.user_id == User.id)
                .where(
                    User.user == maintainer,
                    PagureGroup.group_type == "user",
                    ProjectGroup.access.in_(permissions),
                    *filters,
                )
            )
            query = sa.union(query, sub_q2, sub_q3, sub_q4)

        async with self.Session() as session:
            result = await session.scalars(
                sa.select(Project).where(Project.id.in_(query.scalar_subquery()))
            )
        return [p.as_dict() for p in result]

    @cache(ttl=cache_ttl("pagure"), prefix="v1")
    async def get_user_projects(self, *, username: str) -> list[dict[str, Any]]:
        return await self.get_projects(maintainer=username)

    @cache(
        ttl=cache_ttl("pagure"),
        prefix="v1",
        tags=["pagure:get_project_users:project_path={project_path}"],
    )
    async def get_project_users(
        self, *, project_path: str, roles: PagureRole = PagureRole.USER_ROLES_MAINTAINER
    ) -> list[str]:
        namespace, name = project_path.split("/", 1)
        project_condition = (
            Project.namespace == namespace,
            Project.name == name,
            Project.is_fork.is_(False),
        )
        permissions = [r.name.lower() for r in roles]
        query = (
            sa.select(User.user)
            .join(ProjectUser, ProjectUser.user_id == User.id)
            .join(Project, Project.id == ProjectUser.project_id)
            .where(*project_condition, ProjectUser.access.in_(permissions))
        )
        if PagureRole.OWNER in roles:
            query = sa.union(
                query,
                sa.select(User.user)
                .join(Project, Project.user_id == User.id)
                .where(*project_condition),
            )
        async with self.Session() as session:
            usernames = await session.scalars(query)
        return sorted(set(usernames))

    @cache(
        ttl=cache_ttl("pagure"),
        prefix="v1",
        tags=["pagure:get_project_groups:project_path={project_path}"],
    )
    async def get_project_groups(
        self, *, project_path: str, roles: PagureRole = PagureRole.GROUP_ROLES_MAINTAINER
    ) -> list[str]:
        namespace, name = project_path.split("/", 1)
        project_condition = (
            Project.namespace == namespace,
            Project.name == name,
            Project.is_fork.is_(False),
        )
        permissions = [r.name.lower() for r in roles]
        query = (
            sa.select(PagureGroup.group_name)
            .join(ProjectGroup, ProjectGroup.group_id == PagureGroup.id)
            .join(Project, Project.id == ProjectGroup.project_id)
            .where(*project_condition, ProjectGroup.access.in_(permissions))
            .order_by(PagureGroup.group_name)
        )
        async with self.Session() as session:
            result = await session.scalars(query)
        return list(result)

    @cache(ttl=cache_ttl("pagure"), prefix="v1", tags=["pagure:get_group_projects:name={name}"])
    async def get_group_projects(
        self, *, name: str, acl: PagureRole | None = None
    ) -> list[dict[str, Any]]:
        query = (
            sa.select(Project)
            .join(ProjectGroup, ProjectGroup.project_id == Project.id)
            .join(PagureGroup, PagureGroup.id == ProjectGroup.group_id)
            .where(PagureGroup.group_name == name, Project.is_fork.is_(False))
            .order_by(Project.namespace, Project.name)
        )
        if acl:
            permissions = [role.name.lower() for role in PagureRole.GROUP_ROLES if role & acl]
            query = query.where(
                ProjectGroup.access.in_(permissions),
            )
        async with self.Session() as session:
            projects = await session.scalars(query)
        return [p.as_dict() for p in projects]

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

        if not full_url.startswith(self.base_url):
            # Different Pagure instance
            log.debug("Skipping message for different Pagure instance %s", full_url)
            return

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

            del_tags = [
                f"pagure:get_project_users:project_path={fullname}",
                "pagure:get_projects:maintainer=:owner=",
                f"pagure:get_projects:maintainer={user}",
                f"pagure:get_projects:owner={user}",
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

            del_tags = [
                f"pagure:get_project_groups:project_path={fullname}",
                f"pagure:get_group_projects:name={group}",
            ]

        try:
            await cache.delete_tags(*del_tags)
        except Exception as exc:
            log.warning("Deleting cache entries yielded an exception: %s", exc)


@ft_cache
def get_distgit_proxy(settings: Settings | None = None) -> PagureAsyncProxy:
    settings = settings or get_settings()
    if settings.services.distgit_db_url:
        engine = create_async_engine(settings.services.distgit_db_url, pool_recycle=600)
        return PagureDBProxy(engine, base_url=settings.services.distgit_url)
    else:
        return PagureAsyncProxy(settings.services.distgit_url)
