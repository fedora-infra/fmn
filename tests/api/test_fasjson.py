from unittest import mock

from fmn.api import fasjson


def test_get_fasjson_proxy():
    settings = mock.Mock()
    settings.services.fasjson_url = "http://foo"

    proxy = fasjson.get_fasjson_proxy(settings)

    assert str(proxy.client.base_url).rstrip("/") == "http://foo/v1"
