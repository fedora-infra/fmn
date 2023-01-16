import re

import httpx
import pytest
from fastapi import status

from fmn.core.config import get_settings
from fmn.rules.requester import Requester
from fmn.rules.services.utils import normalize_url


@pytest.fixture
def requester(mocked_fasjson_proxy):
    settings = get_settings()
    return Requester(settings.services)


@pytest.mark.parametrize("url", ["http://srv.example.com/", "http://srv.example.com"])
def test_normalize_url(url):
    assert normalize_url(url) == "http://srv.example.com/"


async def test_handle_http_exception(respx_mocker, requester, caplog):
    respx_mocker.get(re.compile(r"https://src\.fedoraproject\.org/api/.*")).mock(
        return_value=httpx.Response(status.HTTP_500_INTERNAL_SERVER_ERROR, content="Server Error")
    )

    resp = await requester.distgit.get_owned("rpms", "dummy", "user")
    assert resp == []
    assert len(caplog.messages) == 1
    assert caplog.messages[0].startswith(
        "Request failed: Server error '500 Internal Server Error' for url "
        "'https://src.fedoraproject.org/api/"
    )
    assert caplog.records[0].levelname == "WARNING"
