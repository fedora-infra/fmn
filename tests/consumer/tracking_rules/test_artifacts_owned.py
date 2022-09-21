import pytest

from fmn.consumer.tracking_rule import ArtifactsOwned

from ..conftest import Message


@pytest.mark.parametrize(
    "artifact_type",
    [
        "packages",
        "containers",
        "modules",
        "flatpaks",
    ],
)
def test_artifacts_owned(requester, artifact_type):
    tr = ArtifactsOwned(requester, {"username": "dummy"})
    message = Message(topic="dummy", body={artifact_type: ["art-dummy", "art-other"]})
    assert tr.matches(message) is True
    message = Message(topic="dummy", body={artifact_type: ["art-other"]})
    assert tr.matches(message) is False


def test_artifacts_owned_cache(requester, cache):
    tr = ArtifactsOwned(requester, {"username": "dummy"})
    tr.prime_cache(cache)
    assert cache == {
        "packages": set(["package-1", "package-2"]),
        "containers": set(["container-1", "container-2"]),
        "modules": set(["module-1", "module-2"]),
        "flatpaks": set(["flatpak-1", "flatpak-2"]),
    }
