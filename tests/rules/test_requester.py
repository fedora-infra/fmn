from unittest.mock import AsyncMock

import pytest

from fmn.core.config import get_settings
from fmn.rules.requester import Requester
from fmn.rules.services.distgit import DistGitService
from fmn.rules.services.fasjson import FasjsonService


@pytest.fixture
def requester(mocked_fasjson_proxy):
    settings = get_settings()
    return Requester(settings.services)


def test_requester_attributes(mocked_fasjson_proxy):
    requester = Requester(get_settings().services)
    assert hasattr(requester, "distgit")
    assert isinstance(requester.distgit, DistGitService)
    assert hasattr(requester, "fasjson")
    assert isinstance(requester.fasjson, FasjsonService)


async def test_requester_invalidate(mocked_fasjson_proxy):
    requester = Requester(get_settings().services)
    requester.distgit = AsyncMock()
    requester.fasjson = AsyncMock()
    message = object()
    await requester.invalidate_on_message(message)
    requester.distgit.invalidate_on_message.assert_called_once_with(message)
    requester.fasjson.invalidate_on_message.assert_called_once_with(message)
