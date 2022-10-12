import datetime as dt
from unittest import mock

import pytest
from fastapi import status

from fmn.api import api_models, main


@mock.patch("fmn.api.main.get_settings")
@mock.patch("fmn.api.main.app")
def test_add_middlewares(app, get_settings):
    get_settings.return_value = mock.Mock(cors_origins="https://foo")
    main.add_middlewares()

    calls = [
        mock.call(
            main.CORSMiddleware,
            allow_origins=["https://foo"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
    app.add_middleware.assert_has_calls(calls)
    assert app.add_middleware.call_count == 2


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


def test_get_user_info(fasjson_user, fasjson_user_data, client):
    """Test that get_user_info() dispatches to FASJSON."""
    username = fasjson_user_data["username"]
    response = client.get(f"/user/{username}/info")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == fasjson_user_data


@pytest.mark.parametrize("testcase", ("happy-path", "wrong-user"))
def test_get_user_rules(testcase, client, api_identity, db_rule):
    """Verify the results of get_user_rules()."""
    username = api_identity.name
    if testcase == "wrong-user":
        username = f"not-really-{username}"

    response = client.get(f"/user/{username}/rules")

    if testcase == "happy-path":
        assert response.status_code == status.HTTP_200_OK

        results = response.json()
        assert isinstance(results, list)
        assert len(results) == 1

        result = results[0]
        assert result["name"] == db_rule.name
        assert result["tracking_rule"]["name"] == db_rule.tracking_rule.name
        assert result["tracking_rule"]["params"] == db_rule.tracking_rule.params
    elif testcase == "wrong-user":
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert isinstance(response.json()["detail"], str)


@pytest.mark.parametrize("testcase", ("happy-path", "wrong-user"))
def test_get_user_rule(testcase, client, api_identity, db_rule):
    username = api_identity.name
    if testcase == "wrong-user":
        username = f"not-really-{username}"

    response = client.get(f"/user/{username}/rules/{db_rule.id}")

    if testcase == "happy-path":
        assert response.status_code == status.HTTP_200_OK

        result = response.json()
        assert result["name"] == db_rule.name
        assert result["tracking_rule"]["name"] == db_rule.tracking_rule.name
        assert result["tracking_rule"]["params"] == db_rule.tracking_rule.params
    elif testcase == "wrong-user":
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert isinstance(response.json()["detail"], str)


@pytest.mark.parametrize(
    "testcase",
    (
        "success",
        "success-delete-generation-rule",
        "success-delete-destination",
        "success-delete-filter",
        "wrong-user",
    ),
)
def test_edit_user_rule(testcase, client, api_identity, db_rule):
    username = api_identity.name
    if testcase == "wrong-user":
        username = f"not-really-{username}"

    edited_rule = api_models.Rule.from_orm(db_rule)
    edited_rule.tracking_rule.name = "daothertrackingrule"
    if "delete-generation-rule" in testcase:
        del edited_rule.generation_rules[-1]
    elif "delete-destination" in testcase:
        del edited_rule.generation_rules[-1].destinations[-1]
    elif "delete-filter" in testcase:
        del edited_rule.generation_rules[-1].filters.applications
    elif "modify-filter" in testcase:
        edited_rule.generation_rules[-1].filters.applications = ["koji"]
    else:
        edited_rule.generation_rules.append(
            api_models.GenerationRule(destinations=[], filters=api_models.Filters())
        )
        edited_rule.generation_rules[-1].destinations.append(
            api_models.Destination(protocol="foo", address="bar")
        )
        edited_rule.generation_rules[-1].filters.severities = ["very severe"]

    response = client.put(
        f"/user/{username}/rules/{db_rule.id}", data=edited_rule.json(exclude_unset=True)
    )

    if "success" in testcase:
        assert response.status_code == status.HTTP_200_OK

        result = response.json()
        assert result["id"] == edited_rule.id
        assert result["name"] == db_rule.name
        assert result["tracking_rule"]["name"] == "daothertrackingrule"
        assert result["tracking_rule"]["params"] == db_rule.tracking_rule.params
    elif testcase == "wrong-user":
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert isinstance(response.json()["detail"], str)
