import pytest

from fmn.core.constants import ArtifactType
from fmn.rules.tracking_rules import ArtifactsFollowed


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_artifacts_followed(requester, make_mocked_message, artifact_type):
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
    assert tr.matches(msg1) is True
    msg2 = make_mocked_message(
        topic="dummy",
        body={
            msg_attr: ["art2", "art4"],
        },
    )
    assert tr.matches(msg2) is False


def test_artifacts_followed_cache(requester, cache):
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
    tr.prime_cache(cache)
    assert cache == {
        "packages": {"art-1"},
        "containers": {"art-1"},
        "modules": {"art-1"},
        "flatpaks": set(),
    }
