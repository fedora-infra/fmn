from unittest.mock import AsyncMock, Mock

import pytest

from fmn.cache.tracked import Tracked


@pytest.fixture
def requester():
    r = Mock(name="requester")
    r.distgit = AsyncMock(name="distgit")
    r.distgit.get_owners.side_effect = lambda t, n, ug: [n[4:]]
    r.distgit.get_owned.side_effect = lambda t, n, ug: [f"{t}-1", f"{t}-2"]
    r.fasjson = AsyncMock(name="fasjson")
    r.fasjson.get_user_groups.return_value = ["group1"]
    return r


@pytest.fixture
def cache():
    return Tracked()
