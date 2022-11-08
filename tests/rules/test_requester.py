import re

import pytest
import responses

from fmn.core.config import get_settings
from fmn.rules.cache import cache
from fmn.rules.requester import Requester


@pytest.fixture
def requester(mocked_fasjson_client):
    settings = get_settings()
    return Requester(settings.dict()["services"])


def test_constructor_urls(mocked_fasjson_client):
    config = get_settings().dict()["services"].copy()
    config["srv"] = "http://srv.example.com/"
    r = Requester(config)
    assert "srv" in r.urls
    assert r.urls["srv"] == "http://srv.example.com/"


def test_get_owned_by_user(requester):
    responses.get(
        "https://src.fedoraproject.org/api/0/projects?namespace=rpms&owner=dummy&short=1&page=1",
        json={
            "projects": [
                {"name": "project-1"},
                {"name": "project-2"},
            ]
        },
    )
    resp = requester.get_owned_by_user("package", "dummy")
    assert resp == ["project-1", "project-2"]


def test_get_owned_by_group(requester):
    baseurl = (
        "https://src.fedoraproject.org/api/0/projects"
        "?namespace=container&username=@dummy&short=1"
    )
    responses.get(
        baseurl + "&page=1",
        json={
            "projects": [
                {"name": "project-1"},
            ],
            "pagination": {
                "prev": None,
                "next": baseurl + "&page=2",
                "page": 1,
                "pages": 2,
                "per_page": 1,
            },
        },
    )
    responses.get(
        baseurl + "&page=2",
        json={
            "projects": [
                {"name": "project-2"},
            ],
            "pagination": {
                "prev": baseurl + "&page=1",
                "next": None,
                "page": 2,
                "pages": 2,
                "per_page": 1,
            },
        },
    )
    resp = requester.get_owned_by_group("container", "dummy")
    assert resp == ["project-1", "project-2"]


@pytest.mark.parametrize("artifact_type", ["package", "container", "module", "flatpak"])
def test_get_owners(requester, artifact_type):
    responses.get(
        re.compile(r"https://src.fedoraproject.org/api/0/\w+/pkg1"),
        json={"access_users": {"owner": ["dummy"]}},
    )
    method = getattr(requester, f"get_{artifact_type}_owners")
    resp = method("pkg1")
    assert resp == ["dummy"]


@pytest.mark.parametrize("artifact_type", ["package", "container", "module", "flatpak"])
def test_get_group_owners(requester, artifact_type):
    responses.get(
        re.compile(r"https://src.fedoraproject.org/api/0/\w+/pkg1"),
        json={"access_groups": {"admin": ["dummy-1"], "commit": ["dummy-2"]}},
    )
    method = getattr(requester, f"get_{artifact_type}_group_owners")
    resp = method("pkg1")
    assert resp == ["dummy-1", "dummy-2"]


def test_get_user_groups(requester):
    responses.get(
        "https://fasjson.fedoraproject.org/v1/users/dummy/groups/",
        json={
            "result": [
                {"groupname": "group-1"},
                {"groupname": "group-2"},
            ]
        },
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
        (
            "fas.group.member.sponsor",
            {
                "user": "dummy",
            },
        ),
    ],
)
def test_invalidate_on_message(requester, topic, body, mocker, make_mocked_message):
    mocker.patch.object(cache, "region")
    message = make_mocked_message(topic=topic, body=body)
    responses.get(
        "https://src.fedoraproject.org/api/0/rpms/pkg-1",
        json={"access_users": {"owner": []}, "access_groups": {"admin": [], "commit": []}},
    )
    responses.get(
        re.compile(r"https://src.fedoraproject.org/api/0/projects\?.*"),
        json={"projects": []},
    )
    responses.get(
        "https://fasjson.fedoraproject.org/v1/users/dummy/groups/",
        json={"result": []},
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
def test_no_invalidate_on_message(requester, topic, body, mocker, make_mocked_message):
    mocker.patch.object(cache, "region")
    message = make_mocked_message(topic=topic, body=body)
    responses.get(
        "https://src.fedoraproject.org/api/0/rpms/pkg-1",
        json={"access_users": {"owner": []}, "access_groups": {"admin": [], "commit": []}},
    )
    responses.get(
        re.compile(r"https://src.fedoraproject.org/api/0/projects\?.*"),
        json={"projects": []},
    )

    requester.invalidate_on_message(message)
    cache.region.delete.assert_not_called()


def test_guard_bad_argument(requester):
    responses.get(
        "https://src.fedoraproject.org/api/0/rpms/dummy",
        json={},
    )
    with pytest.raises(ValueError):
        requester.distgit_client.get_owners("rpms", "dummy", "wrong")
    with pytest.raises(ValueError):
        requester.distgit_client.get_owned("rpms", "dummy", "wrong")


def test_guard_http_exception(requester, caplog):
    responses.get(
        re.compile(r"https://src\.fedoraproject\.org/api/.*"),
        body="Server Error",
        status=500,
    )
    resp = requester.get_owned_by_user("package", "dummy")
    assert resp == []
    assert len(caplog.messages) == 1
    assert caplog.messages[0].startswith(
        "Request failed: 500 Server Error: Internal Server Error for url: "
        "https://src.fedoraproject.org/api/"
    )
    assert caplog.records[0].levelname == "WARNING"
