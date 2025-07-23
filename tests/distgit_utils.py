# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from fmn.backends.pagure_models import PagureGroup, Project, ProjectGroup, ProjectUser
from fmn.backends.pagure_models import User as PagureUser


async def get_or_create(distgit_proxy, model, search_args, create_args=None):
    create_args = create_args or {}
    async with distgit_proxy.Session() as session:
        try:
            result = await session.execute(
                select(model).where(
                    *[getattr(model, name) == value for name, value in search_args.items()]
                )
            )
            return result.scalar_one()
        except NoResultFound:
            obj = model(**search_args, **create_args)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj


async def distgit_load_projects(distgit_proxy, projects):
    for mocked_project in projects:
        print("Loading project", mocked_project)
        try:
            owner_name = mocked_project["access_users"]["owner"][0]
        except KeyError:
            owner_name = "admin"
        owner = await get_or_create(distgit_proxy, PagureUser, dict(user=owner_name))
        project = await get_or_create(
            distgit_proxy,
            Project,
            dict(
                name=mocked_project["name"],
                namespace=mocked_project["namespace"],
                is_fork=mocked_project.get("is_fork", False),
                user_id=owner.id,
            ),
        )
        for perm, names in mocked_project.get("access_users", {}).items():
            for name in names:
                user = await get_or_create(distgit_proxy, PagureUser, dict(user=name))
                await get_or_create(
                    distgit_proxy,
                    ProjectUser,
                    dict(project_id=project.id, user_id=user.id, access=perm),
                )
        for perm, names in mocked_project.get("access_groups", {}).items():
            for name in names:
                group = await get_or_create(
                    distgit_proxy, PagureGroup, dict(group_name=name), dict(user_id=owner.id)
                )
                await get_or_create(
                    distgit_proxy,
                    ProjectGroup,
                    dict(project_id=project.id, group_id=group.id, access=perm),
                )
