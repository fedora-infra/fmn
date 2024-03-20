# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from itertools import chain
from unittest import mock

import fastapi
import httpx
import pytest

from fmn.backends import PagureAsyncProxy, PagureRole, get_distgit_proxy

from .base import BaseTestAsyncProxy


class TestPagureAsyncProxy(BaseTestAsyncProxy):
    CLS = PagureAsyncProxy
    URL = "https://pagure.test"
    EXPECTED_API_URL = f"{URL}/api/0"

    MOCKED_PROJECTS = [
        {
            "description": "0ad-data containers",
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
            "description": "0install rpms",
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
            "description": "GIMP rpms",
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
    ]

    @pytest.mark.parametrize("testcase", ("normal", "last-page", "pagination-missing"))
    def test_determine_next_page_params(self, testcase, proxy):
        if "normal" in testcase:
            expected_next_url = "/boo"
        else:
            expected_next_url = None

        if "pagination-missing" in testcase:
            result = {}
        elif "last-page" in testcase:
            result = {"pagination": {"next": None}}
        else:
            result = {"pagination": {"next": "/boo?page=2"}}

        params = {}

        next_url, next_params = proxy.determine_next_page_params(
            "/boo", params=params, result=result
        )

        if "normal" in testcase:
            assert next_url == expected_next_url
            assert next_params == params | {"page": "2"}
        else:
            assert next_url is None
            assert next_params is None

    @pytest.mark.parametrize(
        "testcase",
        (
            "filter-by-namespace",
            "filter-by-pattern",
            "filter-by-username",
            "filter-by-owner",
            "no-filter",
        ),
    )
    async def test_get_projects(self, testcase, respx_mocker, proxy_unmocked_client):
        kwargs = {}
        mocked_projects = list(self.MOCKED_PROJECTS)
        if "filter-by-namespace" in testcase:
            kwargs["namespace"] = "rpms"
            mocked_projects = [p for p in mocked_projects if p["namespace"] == "rpms"]
        if "filter-by-pattern" in testcase:
            kwargs["pattern"] = "*0*"
            mocked_projects = [p for p in mocked_projects if "0" in p["name"]]
        if "filter-by-username" in testcase:
            kwargs["username"] = "dudemcpants"
            mocked_projects = [
                p
                for p in mocked_projects
                if any(
                    "dudemcpants" in p["access_users"][acl]
                    for acl in ("admin", "collaborator", "commit", "owner")
                )
            ]
        if "filter-by-owner" in testcase:
            kwargs["owner"] = "dudemcpants"
            mocked_projects = [
                p for p in mocked_projects if "dudemcpants" in p["access_users"]["owner"]
            ]

        params = {"fork": False, "short": True} | kwargs

        route = respx_mocker.get(f"{self.expected_api_url}/projects", params=params).mock(
            side_effect=[
                httpx.Response(fastapi.status.HTTP_200_OK, json={"projects": mocked_projects})
            ]
        )

        artifacts = await proxy_unmocked_client.get_projects(**kwargs)

        assert route.called
        assert artifacts == mocked_projects

        if "filter-by-namespace" in testcase:
            assert all(p["namespace"] == "rpms" for p in mocked_projects)
        if "filter-by-pattern" in testcase:
            assert all("0" in p["name"] for p in mocked_projects)
        if "filter-by-username" in testcase:
            assert all(
                any(
                    "dudemcpants" in users
                    for acl in ("admin", "collaborator", "commit", "owner")
                    for users in p["access_users"][acl]
                )
                for p in mocked_projects
            )
        if "filter-by-owner" in testcase:
            assert all("dudemcpants" in p["access_users"]["owner"] for p in mocked_projects)

    async def test_get_user_projects(self, respx_mocker, proxy_unmocked_client):
        expected_projects = [
            p
            for p in self.MOCKED_PROJECTS
            if any(
                "dudemcpants" in p["access_users"][acl]
                for acl in ("admin", "collaborator", "commit", "owner")
            )
        ]

        params = {"fork": False, "short": False, "username": "dudemcpants"}

        route = respx_mocker.get(f"{self.expected_api_url}/projects", params=params).mock(
            side_effect=[
                httpx.Response(fastapi.status.HTTP_200_OK, json={"projects": self.MOCKED_PROJECTS})
            ]
        )

        artifacts = await proxy_unmocked_client.get_user_projects(username="dudemcpants")

        assert route.called
        assert artifacts == expected_projects

    async def test_get_projects_failure(self, respx_mocker, proxy_unmocked_client):
        route = respx_mocker.get(
            f"{self.expected_api_url}/projects", params={"fork": False, "short": True}
        ).mock(side_effect=httpx.Response(fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR))

        response = await proxy_unmocked_client.get_projects()
        assert route.called
        assert response == []

    @pytest.mark.parametrize("access_role", ("owner", "commit"))
    async def test_get_project_users(self, access_role, respx_mocker, proxy_unmocked_client):
        mocked_project = next(p for p in self.MOCKED_PROJECTS if p["fullname"] == "rpms/gimp")

        route = respx_mocker.get(f"{self.expected_api_url}/rpms/gimp").mock(
            side_effect=[httpx.Response(fastapi.status.HTTP_200_OK, json=mocked_project)]
        )

        users = await proxy_unmocked_client.get_project_users(
            project_path="rpms/gimp", roles=PagureRole[access_role.upper()]
        )

        assert route.called
        assert users == mocked_project["access_users"].get(access_role, [])

    async def test_get_project_users_failure(self, respx_mocker, proxy_unmocked_client):
        route = respx_mocker.get(f"{self.expected_api_url}/rpms/gimp").mock(
            side_effect=[httpx.Response(fastapi.status.HTTP_404_NOT_FOUND)]
        )

        response = await proxy_unmocked_client.get_project_users(project_path="/rpms/gimp")
        assert response == []
        assert route.called

    @pytest.mark.parametrize("access_role", ("owner", "commit"))
    async def test_get_project_groups(self, access_role, respx_mocker, proxy_unmocked_client):
        mocked_project = next(p for p in self.MOCKED_PROJECTS if p["fullname"] == "rpms/gimp")

        route = respx_mocker.get(f"{self.expected_api_url}/rpms/gimp").mock(
            side_effect=[httpx.Response(fastapi.status.HTTP_200_OK, json=mocked_project)]
        )

        groups = await proxy_unmocked_client.get_project_groups(
            project_path="rpms/gimp", roles=PagureRole[access_role.upper()]
        )

        assert route.called
        assert groups == mocked_project["access_groups"].get(access_role, [])

    async def test_get_project_groups_failure(self, respx_mocker, proxy_unmocked_client):
        route = respx_mocker.get(f"{self.expected_api_url}/rpms/gimp").mock(
            side_effect=[httpx.Response(fastapi.status.HTTP_404_NOT_FOUND)]
        )

        response = await proxy_unmocked_client.get_project_groups(project_path="/rpms/gimp")
        assert response == []
        assert route.called

    @pytest.mark.parametrize("access_role", (None, "commit", "ticket"))
    async def test_get_group_projects(self, access_role, respx_mocker, proxy_unmocked_client):
        non_duplicate_projects = [
            p
            for p in self.MOCKED_PROJECTS
            if any(
                "provenpackager" in grouplist
                for groupacl, grouplist in p["access_groups"].items()
                if not access_role or access_role == groupacl
            )
        ]
        if non_duplicate_projects:
            # Ensure there is a duplicate result (due to pagination) to skip over.
            mocked_projects = [*non_duplicate_projects, non_duplicate_projects[-1]]
        else:
            mocked_projects = []

        mocked_group_result = {
            "projects": mocked_projects,
            "pagination": {"prev": None, "next": None, "page": 1, "pages": 1},
        }

        kwargs = {}
        mocked_route_params = {"projects": True}
        if access_role:
            kwargs["acl"] = PagureRole[access_role.upper()]
            mocked_route_params["acl"] = access_role

        route = respx_mocker.get(
            f"{self.expected_api_url}/group/provenpackager", params=mocked_route_params
        ).mock(side_effect=[httpx.Response(fastapi.status.HTTP_200_OK, json=mocked_group_result)])

        projects = await proxy_unmocked_client.get_group_projects(name="provenpackager", **kwargs)

        assert route.called
        assert projects == non_duplicate_projects

    async def test_get_group_projects_failure(self, respx_mocker, proxy_unmocked_client):
        route = respx_mocker.get(f"{self.expected_api_url}/group/provenpackager").mock(
            side_effect=[httpx.Response(fastapi.status.HTTP_404_NOT_FOUND)]
        )

        response = await proxy_unmocked_client.get_group_projects(name="provenpackager")
        assert response == []
        assert route.called

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
    async def test_invalidate_on_message(self, mocker, testcase, proxy, caplog):
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
                    "full_url": "https://pagure.test/rpms/bash",
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
            await proxy.invalidate_on_message(message, None)

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
                    "pagure:get_projects:username=:owner=",
                    "pagure:get_projects:username=the-user",
                    "pagure:get_projects:owner=the-user",
                }
            elif usergroup == "group":
                assert set(args) == {
                    "pagure:get_project_groups:project_path=rpms/bash",
                    "pagure:get_group_projects:name=the-group",
                }

            if "with-exceptions" in testcase:
                assert "Deleting cache entries yielded an exception:" in caplog.text


@mock.patch("fmn.backends.pagure.get_settings")
def test_get_distgit_proxy(get_settings):
    settings = mock.Mock()
    settings.services.distgit_url = "http://foo"
    get_settings.return_value = settings

    proxy = get_distgit_proxy()
    assert str(proxy.client.base_url).rstrip("/") == "http://foo/api/0"

    cached_proxy = get_distgit_proxy()
    assert cached_proxy is proxy

    get_settings.assert_called_once_with()
