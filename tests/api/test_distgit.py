from unittest import mock

import httpx

from fmn.api import distgit


def test_get_distgit_client():
    settings = distgit.Settings(services={"distgit_url": "http://src.distgit.test"})
    distgit_client = distgit.get_distgit_client(settings)
    assert isinstance(distgit_client.client, httpx.AsyncClient)
    assert distgit_client.client.base_url == settings.services.distgit_url


@mock.patch.object(distgit, "AsyncClient")
async def test_get_projects(mock_httpx):
    mock_httpx.return_value = mock_client = mock.AsyncMock()
    mock_client.get.return_value.json = mock.Mock()
    mock_client.get.return_value.json.return_value = {
        "projects": [
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
    }

    settings = distgit.Settings(services={"distgit_url": "http://src.distgit.test"})
    distgit_client = distgit.get_distgit_client(settings)

    artifacts = await distgit_client.get_projects("0")

    mock_client.get.assert_awaited_once_with(
        "/api/0/projects", params={"fork": "false", "pattern": "*0*", "short": "true"}
    )

    assert artifacts == ["0ad-data", "0install"]
