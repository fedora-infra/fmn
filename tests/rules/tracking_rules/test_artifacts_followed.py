import pytest

from fmn.rules.tracking_rules import ArtifactsFollowed


@pytest.mark.parametrize(
    "artifact_type",
    [
        "package",
        "container",
        "module",
        "flatpak",
    ],
)
def test_artifacts_followed(requester, make_mocked_message, artifact_type):
    tr = ArtifactsFollowed(
        requester,
        [{"name": "art1", "type": artifact_type}, {"name": "art3", "type": artifact_type}],
    )
    msg1 = make_mocked_message(
        topic="dummy",
        body={
            f"{artifact_type}s": ["art1", "art2"],
        },
    )
    assert tr.matches(msg1) is True
    msg2 = make_mocked_message(
        topic="dummy",
        body={
            f"{artifact_type}s": ["art2", "art4"],
        },
    )
    assert tr.matches(msg2) is False


def test_artifacts_followed_cache(requester, cache):
    tr = ArtifactsFollowed(
        requester,
        [
            {"name": "art-1", "type": artifact_type}
            for artifact_type in [
                "package",
                "container",
                "module",
            ]
        ],
    )
    tr.prime_cache(cache)
    assert cache == {
        "packages": {"art-1"},
        "containers": {"art-1"},
        "modules": {"art-1"},
        "flatpaks": set(),
    }
