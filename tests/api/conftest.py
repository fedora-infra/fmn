from unittest import mock

import pytest

from fmn.api.config import get_settings


@pytest.fixture(autouse=True)
def clear_api_settings(tmp_path):
    with mock.patch(
        "fmn.api.cli.DEFAULT_CONFIG_FILE", new=str(tmp_path / "non-existing-file")
    ), mock.patch("fmn.api.config.settings_file", new=None):
        get_settings.cache_clear()
        yield
