from fmn.api import fasjson


def test_get_fasjson_client(mocker):
    settings = fasjson.Settings(services={"fasjson_url": "http://fasjson.test/"})
    mocker.patch.object(fasjson.FasjsonClient, "_make_bravado_client")
    client = fasjson.get_fasjson_client(settings)
    assert client._base_url == settings.services.fasjson_url
