# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest import mock

from fmn.core import config


@mock.patch("fmn.core.config.Settings")
def test_get_settings(Settings):
    Settings.return_value = sentinel = object()

    assert config.get_settings() is sentinel

    Settings.assert_called_once_with(_env_file=config.DEFAULT_CONFIG_FILE)
