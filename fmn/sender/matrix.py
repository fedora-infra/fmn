# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
import logging
from contextlib import suppress

from nio import AsyncClient

from .handler import Handler

log = logging.getLogger(__name__)


class MatrixHandler(Handler):
    async def setup(self):
        self._dm_rooms_cache_refresh_task = None
        self._user_id = self._config["user_id"]
        self._client = AsyncClient(self._config["host"], self._user_id)
        # Token login
        self._client.user_id = self._user_id
        self._client.access_token = self._config["token"]
        self._client.device_id = "FMN"
        log.debug("Establishing connection to Matrix")
        await self._client.sync(timeout=30000, full_state=True, set_presence="online")
        log.debug("Synchronized")
        self._dm_rooms_cache = {}
        await self.update_dm_rooms_cache()
        log.debug("Room list updated")
        self.loop = asyncio.get_event_loop()
        # Periodically refresh the DM rooms cache
        self._dm_rooms_cache_refresh_task = self.loop.create_task(self.refresh_dm_rooms_cache())

    async def stop(self):
        log.debug("Stopping Matrix handler...")
        if self._dm_rooms_cache_refresh_task is not None:
            # It is None when the client timeouts connecting to the server
            self._dm_rooms_cache_refresh_task.cancel()
            with suppress(asyncio.TimeoutError, asyncio.CancelledError):
                await asyncio.wait_for(self._dm_rooms_cache_refresh_task, 1)
        await self._client.disconnect()

    async def handle(self, message):
        log.info("Sending message to %s: %s", message["to"], message["message"])
        room_id = await self.get_dm_room(message["to"])
        await self.send_dm(room_id, message["message"])
        await self._client.sync(timeout=30000)

    async def update_dm_rooms_cache(self):
        dm_rooms = {}
        resp = await self._client.joined_rooms()
        for room_id in resp.rooms:
            resp = await self._client.joined_members(room_id)
            if resp.members and len(resp.members) == 2:
                if resp.members[0].user_id == self._user_id:
                    # sndr = resp.members[0]
                    rcvr = resp.members[1]
                elif resp.members[1].user_id == self._user_id:
                    # sndr = resp.members[1]
                    rcvr = resp.members[0]
                else:
                    continue
                dm_rooms[rcvr.user_id] = room_id
        self._dm_rooms_cache = dm_rooms

    async def get_dm_room(self, dest):
        with suppress(KeyError):
            return self._dm_rooms_cache[dest]
        room_id = await self.create_dm_room(dest)
        self._dm_rooms_cache[dest] = room_id
        return room_id

    async def create_dm_room(self, dest):
        resp = await self._client.room_create(is_direct=True, invite=[dest])
        return resp.room_id

    async def send_dm(self, room_id, message):
        await self._client.room_send(
            room_id, message_type="m.room.message", content={"msgtype": "m.text", "body": message}
        )

    async def refresh_dm_rooms_cache(self):
        while True:
            # Do it every day. Sleep first because we're already running it in setup()
            await asyncio.sleep(3600 * 24)
            await self.update_dm_rooms_cache()
