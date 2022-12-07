from unittest import mock

import pytest


@pytest.fixture
def proxy(request):
    test_cls = request.cls
    tested_cls = test_cls.CLS

    proxy = tested_cls(test_cls.URL)
    proxy.client = mock.AsyncMock(base_url=proxy.client.base_url)

    return proxy
