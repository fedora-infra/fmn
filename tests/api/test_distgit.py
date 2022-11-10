import fastapi
import httpx
import pytest

from fmn.core.config import get_settings


def test_get_distgit_client(distgit_client):
    settings = get_settings()
    assert isinstance(distgit_client.client, httpx.AsyncClient)
    assert distgit_client.client.base_url == settings.services.distgit_url


async def test_get_projects(async_respx_mocker, distgit_url, distgit_client):
    mocked_projects = [
        {
            "description": "0ad-data containers",
            "fullname": "containers/0ad-data",
            "name": "0ad-data",
            "namespace": "containers",
        },
        {
            "description": "0install rpms",
            "fullname": "rpms/0install",
            "name": "0install",
            "namespace": "rpms",
        },
    ]
    route = async_respx_mocker.get(
        f"{distgit_url}/api/0/projects", params={"fork": "false", "pattern": "*0*", "short": "true"}
    ).mock(
        side_effect=[
            httpx.Response(
                fastapi.status.HTTP_200_OK,
                json={"projects": mocked_projects},
            )
        ]
    )

    artifacts = await distgit_client.get_projects("0")

    assert route.called
    assert artifacts == mocked_projects


@pytest.mark.parametrize("ownertype", ("user", "group"))
async def test_get_owned_singlepage(async_respx_mocker, distgit_url, distgit_client, ownertype):
    if ownertype == "user":
        param = "owner"
        value = "johnnyjones"
    elif ownertype == "group":
        param = "username"
        value = "@johnnygroup"
    distgit_json_response = {
        "pagination": {"pages": 1, "next": None},
        "projects": [
            {
                "name": "pants",
                "namespace": "rpms",
            },
            {
                "name": "pants",
                "namespace": "flatpaks",
            },
        ],
    }

    params = {"fork": "false", "short": "true", "page": 1, param: value}

    page1_route = async_respx_mocker.get(f"{distgit_url}/api/0/projects", params=params).mock(
        side_effect=[
            httpx.Response(
                fastapi.status.HTTP_200_OK,
                json=distgit_json_response,
            )
        ]
    )

    response = await distgit_client.get_owned([value.lstrip("@")], ownertype)

    assert page1_route.called

    assert response == [
        {"name": "pants", "type": "rpms"},
        {"name": "pants", "type": "flatpaks"},
    ]


@pytest.mark.parametrize("ownertype", ("user", "group"))
async def test_get_owned_twopages(async_respx_mocker, distgit_url, distgit_client, ownertype):
    if ownertype == "user":
        param = "owner"
        val = "johnnyjones"
    elif ownertype == "group":
        param = "username"
        val = "@johnnygroup"
    distgit_json_response = [
        {
            "pagination": {
                "pages": 2,
                "next": f"{distgit_url}/api/0/projects?fork=false&short=true&page=2&{param}={val}",
            },
            "projects": [
                {
                    "name": "trousers",
                    "namespace": "rpms",
                },
                {
                    "name": "trousers",
                    "namespace": "flatpaks",
                },
            ],
        },
        {
            "pagination": {"pages": 2, "next": None},
            "projects": [
                {
                    "name": "pants",
                    "namespace": "rpms",
                },
                {
                    "name": "pants",
                    "namespace": "flatpaks",
                },
            ],
        },
    ]

    params = {"fork": "false", "short": "true", "page": 1, param: val}

    page1_route = async_respx_mocker.get(f"{distgit_url}/api/0/projects", params=params).mock(
        side_effect=[
            httpx.Response(
                fastapi.status.HTTP_200_OK,
                json=distgit_json_response[0],
            )
        ]
    )

    params["page"] = 2
    page2_route = async_respx_mocker.get(f"{distgit_url}/api/0/projects", params=params).mock(
        side_effect=[
            httpx.Response(
                fastapi.status.HTTP_200_OK,
                json=distgit_json_response[1],
            )
        ]
    )

    response = await distgit_client.get_owned([val.lstrip("@")], ownertype)

    assert page1_route.called
    assert page2_route.called

    assert response == [
        {"name": "trousers", "type": "rpms"},
        {"name": "trousers", "type": "flatpaks"},
        {"name": "pants", "type": "rpms"},
        {"name": "pants", "type": "flatpaks"},
    ]


async def test_get_owned_not_user_or_group(distgit_client):
    with pytest.raises(ValueError):
        await distgit_client.get_owned(["johnnyjones"], "not_user_or_group")
