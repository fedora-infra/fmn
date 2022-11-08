import pytest

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
def test_artifacts_owned(requester, make_mocked_message, artifact_type):
    tr = ArtifactsOwned(requester, ["dummy"], "testuser")
    message = make_mocked_message(
        topic="dummy.topic", body={artifact_type: ["art-dummy", "art-other"]}
    )
    assert tr.matches(message) is True
    message = make_mocked_message(topic="dummy.topic", body={artifact_type: ["art-other"]})
    assert tr.matches(message) is False


def test_artifacts_owned_cache(requester, cache):
    tr = ArtifactsOwned(requester, {"username": "dummy"}, "testuser")
    tr.prime_cache(cache)
    assert cache == {
        "packages": set(["package-1", "package-2"]),
        "containers": set(["container-1", "container-2"]),
        "modules": set(["module-1", "module-2"]),
        "flatpaks": set(["flatpak-1", "flatpak-2"]),
    }
