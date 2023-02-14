from enum import Enum


class ArtifactType(Enum):
    # message property → artifact type
    packages = "rpms"
    containers = "containers"
    modules = "modules"
    flatpaks = "flatpaks"


DEFAULT_MATRIX_DOMAIN = "fedora.im"
