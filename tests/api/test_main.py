import datetime as dt
from unittest import mock

import responses

from fmn.api import main


@mock.patch("fmn.api.main.get_settings")
@mock.patch("fmn.api.main.app")
def test_add_middlewares(app, get_settings):
    get_settings.return_value = mock.Mock(cors_origins="https://foo")
    main.add_middlewares()

    app.add_middleware.assert_called_once_with(
        main.CORSMiddleware,
        allow_origins=["https://foo"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def test_read_root():
    request = mock.Mock()
    creds = mock.Mock(scheme="bearer", credentials="abcd-1234")
    identity = mock.Mock(expires_at=dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc))
    identity.name = "foo"  # name can't be set in the constructor of Mock()

    result = await main.read_root(request=request, creds=creds, identity=identity)

    assert result["Hello"] == "World"
    assert result["creds"].scheme == "bearer"
    assert result["creds"].credentials == "abcd-1234"
    assert result["identity"].name == "foo"
    assert isinstance(result["identity"].expires_at, dt.datetime)


def test_get_settings():
    assert isinstance(main.get_settings(), main.Settings)


def test_get_fasjson_client(mocker):
    settings = main.Settings(services={"fasjson_url": "http://fasjson.test/"})
    mocker.patch.object(main.FasjsonClient, "_make_bravado_client")
    client = main.get_fasjson_client(settings)
    assert client._base_url == settings.services.fasjson_url


@responses.activate()
def test_get_userinfo(client, mocker):

    user_data = {
        "username": "dummy",
        "surname": "User",
        "givenname": "Dummy",
        "human_name": "Dummy User",
        "emails": ["dummy@example.test"],
        "ircnicks": ["irc://dummy", "matrix://dummy"],
        "locale": "en-US",
        "uri": "http://fasjson.example.test/v1/users/dummy/",
    }

    responses.get(
        "http://fasjson.example.test/v1/users/dummy/",
        json={"result": user_data},
    )
    response = client.get("/user/dummy/info")
    assert response.status_code == 200
    assert response.json() == user_data
