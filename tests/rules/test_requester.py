import re

import httpx
import pytest
from fastapi import status

from fmn.core.config import get_settings
from fmn.rules.cache import cache
from fmn.rules.requester import Requester


@pytest.fixture
def requester(mocked_fasjson_proxy):
    settings = get_settings()
    return Requester(settings.dict()["services"])


def test_constructor_urls(mocked_fasjson_proxy):
    config = get_settings().dict()["services"].copy()
    config["srv"] = "http://srv.example.com/"
    r = Requester(config)
    assert "srv" in r.urls
    assert r.urls["srv"] == "http://srv.example.com/"


def test_get_owned_by_user(requester, respx_mocker):
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
    resp = requester.get_owned_by_user("packages", "dummy")
    assert resp == ["project-1", "project-2"]


def test_get_owned_by_group(requester, respx_mocker):
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

    resp = requester.get_owned_by_group("container", "dummy")
    assert resp == ["project-1", "project-2"]


@pytest.mark.parametrize("artifact_type", ["package", "container", "module", "flatpak"])
def test_get_owners(requester, artifact_type, respx_mocker):
    respx_mocker.get(re.compile(r"https://src.fedoraproject.org/api/0/\w+/pkg1")).mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={"access_users": {"owner": ["dummy"]}})
    )
    method = getattr(requester, f"get_{artifact_type}_owners")
    resp = method("pkg1")
    assert resp == ["dummy"]


@pytest.mark.parametrize("artifact_type", ["package", "container", "module", "flatpak"])
def test_get_group_owners(requester, artifact_type, respx_mocker):
    respx_mocker.get(re.compile(r"https://src.fedoraproject.org/api/0/\w+/pkg1")).mock(
        return_value=httpx.Response(
            status.HTTP_200_OK,
            json={"access_groups": {"admin": ["dummy-1"], "commit": ["dummy-2"]}},
        )
    )
    method = getattr(requester, f"get_{artifact_type}_group_owners")
    resp = method("pkg1")
    assert resp == ["dummy-1", "dummy-2"]


def test_get_user_groups(requester, respx_mocker, mocked_fasjson_proxy):
    respx_mocker.get("https://fasjson.fedoraproject.org/v1/users/dummy/groups/").mock(
        return_value=httpx.Response(
            status.HTTP_200_OK,
            json={
                "result": [
                    {"groupname": "group-1"},
                    {"groupname": "group-2"},
                ]
            },
        )
    )
    resp = requester.get_user_groups("dummy")
    assert resp == ["group-1", "group-2"]


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
        (
            "fas.group.member.sponsor",
            {
                "user": "dummy",
            },
        ),
    ],
)
def test_invalidate_on_message_user(
    respx_mocker,
    requester,
    topic,
    body,
    mocker,
    make_mocked_message,
    mocked_fasjson_proxy,
):
    mocker.patch.object(cache, "region")
    message = make_mocked_message(topic=topic, body=body)
    respx_mocker.get("https://src.fedoraproject.org/api/0/rpms/pkg-1",).mock(
        return_value=httpx.Response(
            status.HTTP_200_OK,
            json={"access_users": {"owner": []}, "access_groups": {"admin": [], "commit": []}},
        )
    )
    respx_mocker.get(re.compile(r"https://src.fedoraproject.org/api/0/projects\?.*")).mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={"projects": []})
    )
    respx_mocker.get("https://fasjson.fedoraproject.org/v1/users/dummy/groups/").mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={"result": []})
    )

    requester.invalidate_on_message(message)
    cache.region.delete.assert_called_once_with("tracked")


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
                "new_group": "dummy",
            },
        ),
    ],
)
def test_invalidate_on_message_group(
    respx_mocker, requester, topic, body, mocker, make_mocked_message
):
    mocker.patch.object(cache, "region")
    message = make_mocked_message(topic=topic, body=body)
    respx_mocker.get("https://src.fedoraproject.org/api/0/rpms/pkg-1").mock(
        return_value=httpx.Response(
            status.HTTP_200_OK,
            json={"access_users": {"owner": []}, "access_groups": {"admin": [], "commit": []}},
        )
    )
    respx_mocker.get(re.compile(r"https://src.fedoraproject.org/api/0/group/.*\?.*")).mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={"projects": []})
    )
    respx_mocker.get("https://fasjson.fedoraproject.org/v1/users/dummy/groups/").mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={"result": []})
    )

    requester.invalidate_on_message(message)
    cache.region.delete.assert_called_once_with("tracked")


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
    ],
)
def test_no_invalidate_on_message(
    respx_mocker, requester, topic, body, mocker, make_mocked_message
):
    mocker.patch.object(cache, "region")
    message = make_mocked_message(topic=topic, body=body)
    respx_mocker.get("https://src.fedoraproject.org/api/0/rpms/pkg-1").mock(
        return_value=httpx.Response(
            status.HTTP_200_OK,
            json={"access_users": {"owner": []}, "access_groups": {"admin": [], "commit": []}},
        )
    )
    respx_mocker.get(re.compile(r"https://src.fedoraproject.org/api/0/projects\?.*")).mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={"projects": []})
    )

    requester.invalidate_on_message(message)
    cache.region.delete.assert_not_called()


def test_guard_bad_argument(respx_mocker, requester):
    respx_mocker.get("https://src.fedoraproject.org/api/0/rpms/dummy").mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={})
    )
    with pytest.raises(ValueError):
        requester.distgit_client.get_owners("rpms", "dummy", "wrong")
    with pytest.raises(ValueError):
        requester.distgit_client.get_owned("rpms", "dummy", "wrong")


def test_guard_http_exception(respx_mocker, requester, caplog):
    respx_mocker.get(re.compile(r"https://src\.fedoraproject\.org/api/.*")).mock(
        return_value=httpx.Response(status.HTTP_500_INTERNAL_SERVER_ERROR, content="Server Error")
    )
    resp = requester.get_owned_by_user("packages", "dummy")
    assert resp == []
    assert len(caplog.messages) == 1
    assert caplog.messages[0].startswith(
        "Request failed: Server error '500 Internal Server Error' for url "
        "'https://src.fedoraproject.org/api/"
    )
    assert caplog.records[0].levelname == "WARNING"
