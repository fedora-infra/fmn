# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import pytest

from fmn.cache.tracked import Tracked
from fmn.rules.tracking_rules import UsersFollowed


@pytest.mark.parametrize(
    "received,expected",
    [("user1", True), ("user2", False)],
)
async def test_users_followed(requester, make_mocked_message, received, expected):
    tr = UsersFollowed(requester, ["user1"], owner="testuser")
    msg = make_mocked_message(topic="dummy", body={"agent_name": received})
    assert (await tr.matches(msg)) is expected


async def test_users_followed_cache(requester):
    tr = UsersFollowed(requester, ["user1"], owner="testuser")
    cache = Tracked()
    await tr.prime_cache(cache)
    assert cache.agent_name == set(["user1"])
