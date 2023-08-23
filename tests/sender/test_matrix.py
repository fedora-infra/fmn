# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio

import pytest
from nio.responses import JoinedMembersResponse, JoinedRoomsResponse, RoomCreateResponse, RoomMember

from fmn.sender.matrix import MatrixHandler


async def test_matrix_connect(mocker):
    client = mocker.AsyncMock(name="client")
    mocker.patch("fmn.sender.matrix.AsyncClient", return_value=client)
    client.joined_rooms.return_value = JoinedRoomsResponse([])

    handler = MatrixHandler(
        {"host": "matrix.example.com", "user_id": "fmnuser", "token": "dummytoken"}
    )
    await handler.setup()

    assert client.user_id == "fmnuser"
    # S105: Bandit detected a potential password leak. It's not.
    assert client.access_token == "dummytoken"  # noqa: S105
    assert client.device_id == "FMN"
    client.sync.assert_awaited_once_with(timeout=30000, full_state=True, set_presence="online")
    client.joined_rooms.assert_awaited_once_with()

    handler._dm_rooms_cache_refresh_task.cancel()


async def test_matrix_connect_timeout(mocker):
    client = mocker.AsyncMock(name="client")
    mocker.patch("fmn.sender.matrix.AsyncClient", return_value=client)
    client.sync.side_effect = asyncio.exceptions.TimeoutError

    handler = MatrixHandler(
        {"host": "matrix.example.com", "user_id": "fmnuser", "token": "dummytoken"}
    )
    with pytest.raises(asyncio.exceptions.TimeoutError):
        await handler.setup()

    # The CLI calls stop() if the setup() timeouts
    await handler.stop()

    client.disconnect.assert_awaited_once_with()


async def test_matrix_update_dm_rooms_cache(mocker):
    client = mocker.AsyncMock(name="client")
    client.joined_rooms.return_value = JoinedRoomsResponse(
        ["room-1", "room-2", "room-3", "room-4", "room-5"]
    )

    def members_response(room_id):
        if room_id == "room-1":
            members = ["fmnuser"]
        elif room_id == "room-2":
            members = ["fmnuser", "user-1", "user-2"]
        elif room_id == "room-3":
            members = ["user-3", "fmnuser"]
        elif room_id == "room-4":
            members = ["fmnuser", "user-4"]
        elif room_id == "room-5":
            members = ["user-1", "user-2"]
        return JoinedMembersResponse([RoomMember(m, "user", None) for m in members], room_id)

    client.joined_members.side_effect = members_response

    handler = MatrixHandler(
        {"host": "matrix.example.com", "user_id": "fmnuser", "token": "dummytoken"}
    )
    handler._client = client
    handler._user_id = "fmnuser"
    await handler.update_dm_rooms_cache()
    assert handler._dm_rooms_cache == {"user-3": "room-3", "user-4": "room-4"}


async def test_matrix_get_dm_room_from_cache():
    handler = MatrixHandler(
        {"host": "matrix.example.com", "user_id": "fmnuser", "token": "dummytoken"}
    )
    handler._dm_rooms_cache = {"destuser": "dmroom"}
    dm_room = await handler.get_dm_room("destuser")
    assert dm_room == "dmroom"


async def test_matrix_get_dm_room_no_cache(mocker):
    client = mocker.AsyncMock(name="client")
    handler = MatrixHandler(
        {"host": "matrix.example.com", "user_id": "fmnuser", "token": "dummytoken"}
    )
    handler._dm_rooms_cache = {}
    handler._client = client
    client.room_create.return_value = RoomCreateResponse("dmroom")
    dm_room = await handler.get_dm_room("destuser")
    assert dm_room == "dmroom"
    # Must have been created with is_direct and the destination user must be invited
    client.room_create.assert_called_once_with(is_direct=True, invite=["destuser"])
    # Check cache
    assert "destuser" in handler._dm_rooms_cache
    assert handler._dm_rooms_cache["destuser"] == "dmroom"


async def test_matrix_handle(mocker):
    client = mocker.AsyncMock(name="client")
    handler = MatrixHandler(
        {"host": "matrix.example.com", "user_id": "fmnuser", "token": "dummytoken"}
    )
    handler._dm_rooms_cache = {"@destuser:example.com": "dmroom"}
    handler._client = client
    await handler.handle({"to": "@destuser:example.com", "message": "This is a test"})
    client.room_send.assert_awaited_once_with(
        "dmroom",
        message_type="m.room.message",
        content={"msgtype": "m.text", "body": "This is a test"},
    )


async def test_matrix_periodic_refresh(mocker):
    client = mocker.AsyncMock(name="client")
    mocker.patch("fmn.sender.matrix.AsyncClient", return_value=client)
    client.joined_rooms.return_value = JoinedRoomsResponse([])
    handler = MatrixHandler(
        {"host": "matrix.example.com", "user_id": "fmnuser", "token": "dummytoken"}
    )

    real_sleep = asyncio.sleep

    async def fake_sleep(t):
        await real_sleep(0.1)

    mocker.patch("fmn.sender.matrix.asyncio.sleep", side_effect=fake_sleep)
    await handler.setup()
    await real_sleep(1)
    assert client.joined_rooms.call_count > 1
    handler._dm_rooms_cache_refresh_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await asyncio.wait_for(handler._dm_rooms_cache_refresh_task, timeout=1)


async def test_matrix_stop(mocker):
    client = mocker.AsyncMock(name="client")
    handler = MatrixHandler(
        {"host": "matrix.example.com", "user_id": "fmnuser", "token": "dummytoken"}
    )
    handler._dm_rooms_cache_refresh_task = asyncio.create_task(asyncio.sleep(3600))
    handler._client = client
    await handler.stop()
    client.disconnect.assert_awaited_once_with()
    assert handler._dm_rooms_cache_refresh_task.cancelled() is True
