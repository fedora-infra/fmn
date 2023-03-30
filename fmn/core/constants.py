# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from enum import Enum
from functools import cache


class ArtifactType(Enum):
    # message property → artifact type
    packages = "rpms"
    containers = "containers"
    modules = "modules"
    flatpaks = "flatpaks"

    @classmethod
    @cache
    def has_value(cls, value):
        try:
            cls(value)
        except ValueError:
            return False
        return True


DEFAULT_MATRIX_DOMAIN = "fedora.im"
