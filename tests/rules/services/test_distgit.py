import re

import httpx
import pytest
from cashews import cache
from cashews.formatter import get_templates_for_func
from fastapi import status

from fmn.cache.tracked import TrackedCache
from fmn.rules.services.distgit import DistGitService


@pytest.fixture
def service():
    return DistGitService("https://src.fedoraproject.org")


tracked_cache_key = list(get_templates_for_func(TrackedCache.get_tracked))[0]


async def test_get_owned_by_user(service, respx_mocker):
    respx_mocker.get(
        "https://src.fedoraproject.org/api/0/projects?namespace=rpms&owner=dummy&short=1"
    ).mock(
        return_value=httpx.Response(
            status.HTTP_200_OK,
            json={
                "projects": [
                    {"name": "project-1"},
                    {"name": "project-2"},
                ]
            },
        )
    )
    resp = await service.get_owned("rpms", "dummy", "user")
    assert resp == ["project-1", "project-2"]


async def test_get_owned_by_group(service, respx_mocker):
    baseurl = "https://src.fedoraproject.org/api/0/group/dummy?projects=true"

    num_projects = 2
    for num in range(1, num_projects + 1):
        urls = [baseurl + f"&page={num}"]
        if num == 1:
            urls.append(baseurl)
        for url in urls:
            respx_mocker.get(url).mock(
                return_value=httpx.Response(
                    status.HTTP_200_OK,
                    json={
                        "projects": [
                            {"name": f"project-{num}"},
                        ],
                        "pagination": {
                            "prev": None if num == 1 else baseurl + f"&page={num - 1}",
                            "next": None if num == num_projects else baseurl + f"&page={num + 1}",
                            "page": num,
                            "pages": num_projects,
                            "per_page": 1,
                        },
                    },
                )
            )

    resp = await service.get_owned("container", "dummy", "group")
    assert resp == ["project-1", "project-2"]


@pytest.mark.parametrize("artifact_type", ["rpms", "containers", "modules", "flatpaks"])
async def test_get_owners(service, artifact_type, respx_mocker):
    respx_mocker.get(re.compile(r"https://src.fedoraproject.org/api/0/\w+/pkg1")).mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={"access_users": {"owner": ["dummy"]}})
    )
    resp = await service.get_owners(artifact_type, "pkg1", "user")
    assert resp == ["dummy"]


@pytest.mark.parametrize("artifact_type", ["rpms", "containers", "modules", "flatpaks"])
async def test_get_group_owners(service, artifact_type, respx_mocker):
    respx_mocker.get(re.compile(r"https://src.fedoraproject.org/api/0/\w+/pkg1")).mock(
        return_value=httpx.Response(
            status.HTTP_200_OK,
            json={"access_groups": {"admin": ["dummy-1"], "commit": ["dummy-2"]}},
        )
    )
    resp = await service.get_owners(artifact_type, "pkg1", "group")
    assert resp == ["dummy-1", "dummy-2"]


@pytest.mark.parametrize(
    "topic,body",
    [
        (
            "pagure.project.user.access.updated",
            {
                "new_access": "owner",
                "new_user": "dummy",
                "project": {"namespace": "rpms", "name": "pkg-1"},
            },
        ),
        (
            "pagure.project.user.added",
            {
                "new_user": "dummy",
                "project": {
                    "namespace": "rpms",
                    "name": "pkg-1",
                    "access_users": {"owner": ["dummy"]},
                },
            },
        ),
    ],
)
async def test_invalidate_on_message_user(
    respx_mocker,
    service,
    topic,
    body,
    mocker,
    make_mocked_message,
):
    mocker.patch.object(cache, "delete")
    message = make_mocked_message(topic=topic, body=body)
    await service.invalidate_on_message(message)
    cache.delete.assert_called_once_with(tracked_cache_key)


@pytest.mark.parametrize(
    "topic,body",
    [
        (
            "pagure.project.group.access.updated",
            {
                "new_access": "commit",
                "new_group": "dummy",
                "project": {"namespace": "rpms", "name": "pkg-1"},
            },
        ),
        (
            "pagure.project.group.added",
            {
                "new_group": "dummy",
                "project": {
                    "namespace": "rpms",
                    "name": "pkg-1",
                    "access_groups": {"admin": ["dummy"], "commit": ["dummy-2"]},
                },
            },
        ),
        (
            "pagure.project.group.removed",
            {
                "access": "commit",
                "project": {"namespace": "rpms", "name": "pkg-1"},
                "removed_groups": ["dummy"],
            },
        ),
    ],
)
async def test_invalidate_on_message_group(
    respx_mocker, service, topic, body, mocker, make_mocked_message
):
    mocker.patch.object(cache, "delete")
    message = make_mocked_message(topic=topic, body=body)
    await service.invalidate_on_message(message)
    cache.delete.assert_called_once_with(tracked_cache_key)


@pytest.mark.parametrize(
    "topic,body",
    [
        (
            "pagure.project.user.access.updated",
            {
                "new_access": "committer",
            },
        ),
        (
            "pagure.project.user.added",
            {
                "new_user": "dummy",
                "project": {
                    "access_users": {"owner": ["someone-else"]},
                },
            },
        ),
        (
            "pagure.project.group.access.updated",
            {
                "new_access": "ticket",
            },
        ),
        (
            "pagure.project.group.added",
            {
                "new_group": "dummy",
                "project": {
                    "access_groups": {"admin": [], "commit": []},
                },
            },
        ),
        (
            "pagure.project.group.removed",
            {
                "access": "ticket",
            },
        ),
        (
            "something.unrelated",
            {
                "foo": "bar",
            },
        ),
    ],
)
async def test_no_invalidate_on_message(
    respx_mocker, service, topic, body, mocker, make_mocked_message
):
    mocker.patch.object(cache, "delete")
    message = make_mocked_message(topic=topic, body=body)
    await service.invalidate_on_message(message)
    cache.delete.assert_not_called()


async def test_guard_bad_argument(respx_mocker, service):
    respx_mocker.get("https://src.fedoraproject.org/api/0/rpms/dummy").mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={})
    )
    with pytest.raises(ValueError):
        await service.get_owners("rpms", "dummy", "wrong")
    with pytest.raises(ValueError):
        await service.get_owned("rpms", "dummy", "wrong")
