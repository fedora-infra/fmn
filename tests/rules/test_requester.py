# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest.mock import AsyncMock

import pytest

from fmn.backends import FASJSONAsyncProxy, PagureAsyncProxy
from fmn.rules.requester import Requester


@pytest.fixture
def requester(mocked_fasjson_proxy):
    return Requester()


def test_requester_attributes(mocked_fasjson_proxy):
    requester = Requester()
    assert hasattr(requester, "distgit")
    assert isinstance(requester.distgit, PagureAsyncProxy)
    assert hasattr(requester, "fasjson")
    assert isinstance(requester.fasjson, FASJSONAsyncProxy)


async def test_requester_invalidate(mocked_fasjson_proxy):
    requester = Requester()
    requester.distgit = AsyncMock()
    requester.fasjson = AsyncMock()
    message = object()
    db = object()
    await requester.invalidate_on_message(message, db)
    requester.distgit.invalidate_on_message.assert_called_once_with(message, db)
    requester.fasjson.invalidate_on_message.assert_called_once_with(message, db)
