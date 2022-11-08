import pytest

from fmn.rules.tracking_rules import ArtifactsGroupOwned


@pytest.mark.parametrize(
    "artifact_type",
    [
        "packages",
        "containers",
        "modules",
        "flatpaks",
    ],
)
def test_artifacts_group_owned(requester, make_mocked_message, artifact_type):
    tr = ArtifactsGroupOwned(requester, ["group1"], owner="testuser")
    message = make_mocked_message(topic="dummy", body={artifact_type: ["art-group1", "art-group2"]})
    assert tr.matches(message) is True
    message = make_mocked_message(topic="dummy", body={artifact_type: ["art-group2"]})
    assert tr.matches(message) is False


def test_artifacts_group_owned_cache(requester, cache):
    tr = ArtifactsGroupOwned(requester, ["group1"], owner="testuser")
    tr.prime_cache(cache)
    assert cache == {
        "packages": set(["packages-1", "packages-2"]),
        "containers": set(["containers-1", "containers-2"]),
        "modules": set(["modules-1", "modules-2"]),
        "flatpaks": set(["flatpaks-1", "flatpaks-2"]),
    }
