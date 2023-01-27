import pytest

from fmn.core.config import get_settings
from fmn.rules.requester import Requester
from fmn.rules.services import utils


@pytest.fixture
def requester(mocked_fasjson_proxy):
    settings = get_settings()
    return Requester(settings.services)


@pytest.mark.parametrize("testcase", ("success", "raises-exception"))
async def test_handle_http_error(testcase, mocker):
    mocker.patch.object(utils, "httpx")

    class MockException(Exception):
        pass

    utils.httpx.HTTPStatusError = MockException

    if "raises-exception" in testcase:

        async def fn_to_be_decorated():
            raise MockException("BOO")

    else:

        async def fn_to_be_decorated():
            return ["item"]

    decorated_fn = utils.handle_http_error(list)(fn_to_be_decorated)

    result = await decorated_fn()

    if "success" in testcase:
        assert result == ["item"]
    else:
        assert result == []


@pytest.mark.parametrize("url", ["http://srv.example.com/", "http://srv.example.com"])
def test_normalize_url(url):
    assert utils.normalize_url(url) == "http://srv.example.com/"
