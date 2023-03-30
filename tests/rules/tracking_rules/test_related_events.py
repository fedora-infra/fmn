# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import pytest

from fmn.cache.tracked import Tracked
from fmn.rules.tracking_rules import RelatedEvents


@pytest.mark.parametrize(
    "received,expected",
    [(["user1", "user2"], True), (["user2"], False)],
)
async def test_related_events(requester, make_mocked_message, received, expected):
    tr = RelatedEvents(requester, None, "user1")
    msg = make_mocked_message(topic="dummy", body={"usernames": received})
    assert (await tr.matches(msg)) is expected


async def test_users_followed_cache(requester):
    tr = RelatedEvents(requester, None, "testuser")
    cache = Tracked()
    await tr.prime_cache(cache)
    assert cache.usernames == set(["testuser"])
