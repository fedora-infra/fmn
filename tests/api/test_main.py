import responses

from fmn.api import main


def test_read_root():
    assert main.read_root()["Hello"] == "World"


def test_get_settings():
    assert isinstance(main.get_settings(), main.Settings)


def test_get_fasjson_client(mocker):
    settings = main.Settings(fasjson_url="http://fasjson.test/")
    mocker.patch.object(main.FasjsonClient, "_make_bravado_client")
    client = main.get_fasjson_client(settings)
    assert client._base_url == settings.fasjson_url


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
