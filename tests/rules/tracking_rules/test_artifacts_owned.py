# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import pytest

from fmn.cache.tracked import Tracked
from fmn.rules.tracking_rules import ArtifactsOwned


@pytest.mark.parametrize(
    "artifact_type",
    [
        "packages",
        "containers",
        "modules",
        "flatpaks",
    ],
)
async def test_artifacts_owned(requester, make_mocked_message, artifact_type):
    tr = ArtifactsOwned(requester, ["dummy"], "testuser")
    message = make_mocked_message(
        topic="dummy.topic", body={artifact_type: ["art-dummy", "art-other"]}
    )
    assert (await tr.matches(message)) is True
    message = make_mocked_message(topic="dummy.topic", body={artifact_type: ["art-other"]})
    assert (await tr.matches(message)) is False


async def test_artifacts_owned_cache(requester, cache):
    tr = ArtifactsOwned(requester, ["dummy"], "testuser")
    await tr.prime_cache(cache)
    assert cache == Tracked(
        packages=set(["rpms-1", "rpms-2"]),
        containers=set(["containers-1", "containers-2"]),
        modules=set(["modules-1", "modules-2"]),
        flatpaks=set(["flatpaks-1", "flatpaks-2"]),
    )
