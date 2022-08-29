from unittest import mock

from fmn.api import config


@mock.patch("fmn.api.config.Settings")
def test_get_settings(Settings):
    Settings.return_value = sentinel = object()

    assert config.get_settings() is sentinel

    Settings.assert_called_once_with(_env_file=None)
