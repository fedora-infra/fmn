import httpx
import pytest
from cashews import cache
from cashews.formatter import get_templates_for_func
from fastapi import status

from fmn.cache.tracked import TrackedCache
from fmn.rules.services.fasjson import FasjsonService


@pytest.fixture
def service():
    return FasjsonService("https://fasjson.fedoraproject.org")


tracked_cache_key = list(get_templates_for_func(TrackedCache.get_tracked))[0]


async def test_get_user_groups(service, respx_mocker, mocked_fasjson_proxy):
    mocked_req = respx_mocker.get("https://fasjson.fedoraproject.org/v1/users/dummy/groups/").mock(
        return_value=httpx.Response(
            status.HTTP_200_OK,
            json={
                "result": [
                    {"groupname": "group-1"},
                    {"groupname": "group-2"},
                ]
            },
        )
    )
    resp = await service.get_user_groups("dummy")
    assert resp == ["group-1", "group-2"]
    mocked_req.calls.assert_called_once()


@pytest.mark.parametrize(
    "topic,body",
    [
        (
            "fas.group.member.sponsor",
            {
                "user": "dummy",
            },
        ),
    ],
)
async def test_invalidate_on_message_user(
    respx_mocker,
    service,
    topic,
    body,
    mocker,
    make_mocked_message,
    mocked_fasjson_proxy,
):
    mocker.patch.object(cache, "delete")
    message = make_mocked_message(topic=topic, body=body)
    mocked_req = respx_mocker.get("https://fasjson.fedoraproject.org/v1/users/dummy/groups/").mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={"result": []})
    )

    await service.invalidate_on_message(message)
    cache.delete.assert_called_once_with(tracked_cache_key)
    mocked_req.calls.assert_called_once()


@pytest.mark.parametrize(
    "topic,body",
    [
        (
            "something.unrelated",
            {
                "foo": "bar",
            },
        ),
    ],
)
async def test_no_invalidate_on_message(
    service,
    topic,
    body,
    mocker,
    make_mocked_message,
    mocked_fasjson_proxy,
):
    mocker.patch.object(cache, "delete")
    message = make_mocked_message(topic=topic, body=body)

    await service.invalidate_on_message(message)
    cache.delete.assert_not_called
