# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from pathlib import Path

import toml

HERE = Path(__file__).parent
PYPROJECT_TOML_PATH = HERE.parent.parent / "pyproject.toml"


def test___version__():
    from fmn.core.version import __version__

    pyproject = toml.load(PYPROJECT_TOML_PATH)

    assert __version__ == pyproject["tool"]["poetry"]["version"]
