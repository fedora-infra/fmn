# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import pytest

from fmn.cache.tracked import Tracked
from fmn.core.constants import ArtifactType
from fmn.rules.tracking_rules import ArtifactsFollowed


@pytest.mark.parametrize("artifact_type", ArtifactType)
async def test_artifacts_followed(requester, make_mocked_message, artifact_type):
    msg_attr = artifact_type.name
    tr = ArtifactsFollowed(
        requester,
        [
            {"name": "art1", "type": artifact_type.value},
            {"name": "art3", "type": artifact_type.value},
        ],
        owner="testuser",
    )
    msg1 = make_mocked_message(
        topic="dummy",
        body={
            msg_attr: ["art1", "art2"],
        },
    )
    assert (await tr.matches(msg1)) is True
    msg2 = make_mocked_message(
        topic="dummy",
        body={
            msg_attr: ["art2", "art4"],
        },
    )
    assert (await tr.matches(msg2)) is False


async def test_artifacts_followed_cache(requester, cache):
    tr = ArtifactsFollowed(
        requester,
        [
            {"name": "art-1", "type": artifact_type}
            for artifact_type in [
                "rpms",
                "containers",
                "modules",
            ]
        ],
        owner="testuser",
    )
    await tr.prime_cache(cache)
    assert cache == Tracked(
        packages={"art-1"},
        containers={"art-1"},
        modules={"art-1"},
    )
