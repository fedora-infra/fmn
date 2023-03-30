# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest import mock

import pytest


def _create_proxy_for_request(request):
    test_cls = request.cls
    tested_cls = test_cls.CLS

    return tested_cls(test_cls.URL)


@pytest.fixture
def proxy_unmocked_client(request):
    """Instantiate a proxy as defined in the test class."""
    return _create_proxy_for_request(request)


@pytest.fixture
def proxy(request):
    """Instantiate a proxy as defined in the test class with a mocked client."""
    proxy = _create_proxy_for_request(request)
    proxy.client = mock.AsyncMock(base_url=proxy.client.base_url)

    return proxy
