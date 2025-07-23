# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from itertools import chain
from unittest import mock

import pytest

from fmn.backends import PagureRole, get_distgit_proxy
from fmn.backends.pagure_models import Project, User

from ..distgit_utils import distgit_load_projects


def _get_expected(distgit_projects):
    return [
        {key: value for key, value in project.items() if not key.startswith("access_")}
        for project in distgit_projects
    ]


@pytest.fixture()
async def distgit_projects(distgit_proxy):
    MOCKED_PROJECTS = [
        {
            "fullname": "containers/0ad-data",
            "name": "0ad-data",
            "namespace": "containers",
            "access_users": {
                "admin": [],
                "collaborator": [],
                "commit": [],
                "owner": ["dudemcpants"],
                "ticket": [],
            },
            "access_groups": {
                "admin": [],
                "collaborator": [],
                "commit": [],
                "ticket": [],
            },
        },
        {
            "fullname": "rpms/0install",
            "name": "0install",
            "namespace": "rpms",
            "access_users": {
                "admin": [],
                "collaborator": [],
                "commit": [],
                "owner": ["dudettemcpants"],
                "ticket": [],
            },
            "access_groups": {
                "admin": [],
                "collaborator": [],
                "commit": [],
                "ticket": [],
            },
        },
        {
            "fullname": "rpms/gimp",
            "name": "gimp",
            "namespace": "rpms",
            "access_users": {
                "admin": [],
                "collaborator": [],
                "commit": [],
                "owner": ["wilber"],
                "ticket": [],
            },
            "access_groups": {
                "admin": [],
                "collaborator": [],
                "commit": ["provenpackager"],
                "ticket": [],
            },
        },
        # A fork of rpms/gimp
        {
            "fullname": "rpms/gimp",
            "name": "gimp",
            "namespace": "rpms",
            "is_fork": True,
            "access_users": {
                "admin": [],
                "collaborator": [],
                "commit": [],
                "owner": ["dummy-fork-owner"],
                "ticket": [],
            },
            "access_groups": {
                "admin": [],
                "collaborator": [],
                "commit": ["provenpackager"],
                "ticket": [],
            },
        },
    ]
    await distgit_load_projects(distgit_proxy, MOCKED_PROJECTS)
    return MOCKED_PROJECTS


class TestPagureDBProxy:

    @pytest.mark.parametrize(
        "testcase",
        (
            "filter-by-namespace",
            "filter-by-pattern",
            "filter-by-name",
            "filter-by-username",
            "filter-by-owner",
            "no-filter",
        ),
    )
    async def test_get_projects(self, testcase, distgit_proxy, distgit_projects):
        kwargs = {}
        distgit_projects = [p for p in distgit_projects if not p.get("is_fork", False)]
        if "filter-by-namespace" in testcase:
            kwargs["namespace"] = "rpms"
            distgit_projects = [p for p in distgit_projects if p["namespace"] == "rpms"]
        if "filter-by-pattern" in testcase:
            kwargs["pattern"] = "*0*"
            distgit_projects = [p for p in distgit_projects if "0" in p["name"]]
        if "filter-by-name" in testcase:
            kwargs["pattern"] = "gimp"
            distgit_projects = [p for p in distgit_projects if p["name"] == "gimp"]
        if "filter-by-username" in testcase:
            kwargs["maintainer"] = "dudemcpants"
            distgit_projects = [
                p
                for p in distgit_projects
                if any(
                    "dudemcpants" in p["access_users"][acl]
                    for acl in ("admin", "collaborator", "commit", "owner")
                )
            ]
        if "filter-by-owner" in testcase:
            kwargs["owner"] = "dudemcpants"
            distgit_projects = [
                p for p in distgit_projects if "dudemcpants" in p["access_users"]["owner"]
            ]

        artifacts = await distgit_proxy.get_projects(**kwargs)
        assert artifacts == _get_expected(distgit_projects)

    async def test_get_user_projects(self, distgit_proxy, distgit_projects):
        expected_projects = _get_expected(
            [
                p
                for p in distgit_projects
                if any(
                    "dudemcpants" in p["access_users"][acl]
                    for acl in ("admin", "collaborator", "commit", "owner")
                )
            ]
        )
        artifacts = await distgit_proxy.get_user_projects(username="dudemcpants")
        assert artifacts == expected_projects

    @pytest.mark.parametrize("access_role", ("owner", "commit"))
    async def test_get_project_users(self, access_role, distgit_proxy, distgit_projects):
        mocked_project = next(p for p in distgit_projects if p["fullname"] == "rpms/gimp")

        users = await distgit_proxy.get_project_users(
            project_path="rpms/gimp", roles=PagureRole[access_role.upper()]
        )
        assert users == mocked_project["access_users"].get(access_role, [])

    async def test_get_project_users_failure(self, distgit_proxy, distgit_projects):
        response = await distgit_proxy.get_project_users(project_path="/rpms/does-not-exist")
        assert response == []

    # async def test_get_project_users_forks(self, distgit_proxy, distgit_projects):
    #     forked_repo = {
    #         "fullname": "rpms/gimp",
    #         "name": "gimp",
    #         "namespace": "rpms",
    #         "is_fork": True,
    #         "access_users": {
    #             "admin": [],
    #             "collaborator": [],
    #             "commit": [],
    #             "owner": ["dummy-fork-owner"],
    #             "ticket": [],
    #         },
    #     }
    #     await distgit_load_projects(distgit_proxy, [forked_repo])
    #     mocked_project = next(p for p in distgit_projects if p["fullname"] == "rpms/gimp")
    #     users = await distgit_proxy.get_project_users(
    #         project_path="rpms/gimp", roles=PagureRole.OWNER
    #     )
    #     assert users == mocked_project["access_users"].get("owner", [])

    @pytest.mark.parametrize("access_role", ("owner", "commit"))
    async def test_get_project_groups(self, access_role, distgit_proxy, distgit_projects):
        mocked_project = next(p for p in distgit_projects if p["fullname"] == "rpms/gimp")

        groups = await distgit_proxy.get_project_groups(
            project_path="rpms/gimp", roles=PagureRole[access_role.upper()]
        )
        assert groups == mocked_project["access_groups"].get(access_role, [])

    async def test_get_project_groups_failure(self, distgit_proxy, distgit_projects):
        response = await distgit_proxy.get_project_groups(project_path="/rpms/does-not-exist")
        assert response == []

    async def test_get_project_groups_fork(self, distgit_proxy, distgit_projects):
        mocked_project = next(p for p in distgit_projects if p["fullname"] == "rpms/gimp")

        groups = await distgit_proxy.get_project_groups(
            project_path="rpms/gimp", roles=PagureRole.OWNER
        )
        assert groups == mocked_project["access_groups"].get("owner", [])

    @pytest.mark.parametrize("access_role", (None, "commit", "ticket"))
    async def test_get_group_projects(self, access_role, distgit_proxy, distgit_projects):
        non_duplicate_projects = _get_expected(
            [
                p
                for p in distgit_projects
                if not p.get("is_fork", False)
                and any(
                    "provenpackager" in grouplist
                    for groupacl, grouplist in p["access_groups"].items()
                    if not access_role or access_role == groupacl
                )
            ]
        )

        kwargs = {}
        if access_role:
            kwargs["acl"] = PagureRole[access_role.upper()]

        projects = await distgit_proxy.get_group_projects(name="provenpackager", **kwargs)

        assert projects == non_duplicate_projects

    async def test_get_group_projects_failure(self, distgit_proxy, distgit_projects):
        response = await distgit_proxy.get_group_projects(name="does-not-exist")
        assert response == []

    @pytest.mark.parametrize(
        "testcase",
        chain(
            (
                pytest.param((testcase, usergroup, action), id=f"{testcase}-{usergroup}-{action}")
                for testcase in ("success", "failure-missing-affected")
                for usergroup in ("user", "group")
                for action in ("access.updated", "added", "removed")
            ),
            (
                "skip-other-topic",
                "failure-missing-project",
                "failure-missing-fullname",
                "failure-missing-full_url",
                "skip-other-pagure-instance",
                "success-ish-with-exceptions",
            ),
        ),
    )
    async def test_invalidate_on_message(
        self, mocker, testcase, caplog, distgit_proxy, distgit_projects
    ):
        cache = mocker.patch("fmn.backends.pagure.cache")
        cache.delete_tags = mock.AsyncMock()

        if isinstance(testcase, tuple):
            testcase, usergroup, action = testcase
        else:
            usergroup = "user"
            action = "access.updated"

        if "with-exceptions" in testcase:
            cache.delete_tags.side_effect = RuntimeError("BOO")

        # basic (incomplete) message
        message = mock.Mock(
            topic=f"org.fedoraproject.prod.pagure.project.{usergroup}.{action}",
            body={
                "project": {
                    "fullname": "rpms/bash",
                    "full_url": "https://distgit.test/rpms/bash",
                },
            },
        )
        body = message.body
        project = body["project"]

        # Complete the message or muck it up, depending on testcase.
        if "failure-missing-affected" not in testcase:
            if action == "removed":
                if usergroup == "group":
                    # Pagure will send a list of group names, but looking at the code, it can only
                    # be one.
                    body["removed_groups"] = ["the-group"]
                else:
                    body["removed_user"] = "the-user"
            else:
                body[f"new_{usergroup}"] = f"the-{usergroup}"

        match testcase:
            case "skip-other-topic":
                message.topic = "this.is.not.the.message.you’re.looking.for"
            case "failure-missing-project":
                del body["project"]
            case "failure-missing-fullname":
                del project["fullname"]
            case "failure-missing-full_url":
                del project["full_url"]
            case "skip-other-pagure-instance":
                project["full_url"] = "https://pagure.io/fedora-infra/ansible"

        with caplog.at_level(logging.DEBUG):
            await distgit_proxy.invalidate_on_message(message, None)

        if "success" not in testcase:
            cache.delete_tags.assert_not_called()

            if "missing-affected" in testcase:
                assert f"No affected {usergroup} found" in caplog.text
            elif "other-topic" in testcase:
                assert "Skipping message with topic" in caplog.text
            elif "missing-project" in testcase:
                assert "No project info found" in caplog.text
            elif "missing-fullname" in testcase:
                assert "No full name found for affected project" in caplog.text
            elif "missing-full_url" in testcase:
                assert "No URL found for affected project" in caplog.text
            elif "other-pagure-instance" in testcase:
                assert "Skipping message for different Pagure instance" in caplog.text
        else:
            cache.delete_tags.assert_awaited_once()
            args, _ = cache.delete_tags.await_args
            if usergroup == "user":
                assert set(args) == {
                    "pagure:get_project_users:project_path=rpms/bash",
                    "pagure:get_projects:maintainer=:owner=",
                    "pagure:get_projects:maintainer=the-user",
                    "pagure:get_projects:owner=the-user",
                }
            elif usergroup == "group":
                assert set(args) == {
                    "pagure:get_project_groups:project_path=rpms/bash",
                    "pagure:get_group_projects:name=the-group",
                }

            if "with-exceptions" in testcase:
                assert "Deleting cache entries yielded an exception:" in caplog.text

    async def test_start_stop(self, distgit_proxy):
        await distgit_proxy.start()
        await distgit_proxy._engine.dispose()
        distgit_proxy._engine = mock.AsyncMock()
        await distgit_proxy.stop()
        distgit_proxy._engine.dispose.assert_awaited_once_with()


@mock.patch("fmn.backends.pagure.get_settings")
def test_get_distgit_proxy(get_settings):
    settings = mock.Mock()
    settings.services.distgit_db_url = "sqlite+aiosqlite:////foo"
    settings.services.distgit_url = "https://distgit.test"
    get_settings.return_value = settings

    proxy = get_distgit_proxy()
    assert str(proxy.Session().get_bind().url) == "sqlite+aiosqlite:////foo"

    cached_proxy = get_distgit_proxy()
    assert cached_proxy is proxy

    get_settings.assert_called_once_with()


@pytest.mark.parametrize(
    ["namespace", "is_fork", "expected"],
    [
        (None, False, "dummy-name"),
        ("ns", False, "ns/dummy-name"),
        (None, True, "forks/dummy-user/dummy-name"),
        ("ns", True, "forks/dummy-user/dummy-name"),
    ],
)
def test_pagure_model_project_fullname(namespace, is_fork, expected):
    user = User(user="dummy-user")
    project = Project(name="dummy-name", user=user, namespace=namespace, is_fork=is_fork)
    assert project.fullname == expected
