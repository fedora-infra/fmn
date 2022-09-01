import json
import os
from unittest import mock

import pytest
import responses
from click.testing import CliRunner
from fastapi.testclient import TestClient

from fmn.api import main
from fmn.core.config import Settings, get_settings


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def client():
    def get_settings_override():
        return Settings(fasjson_url="http://fasjson.example.test")

    def get_fasjson_client_override():
        responses.add_passthru("https://json-schema.org")
        fasjson_spec_path = os.path.join(os.path.dirname(__file__), "fixtures", "fasjson-v1.json")
        with open(fasjson_spec_path) as fasjson_spec_file:
            fasjson_spec = json.load(fasjson_spec_file)
        responses.get("http://fasjson.example.test/specs/v1.json", json=fasjson_spec)
        base_url = get_settings_override().fasjson_url

        return main.FasjsonClient(base_url, auth=False)

    main.app.dependency_overrides[main.get_settings] = get_settings_override
    main.app.dependency_overrides[main.get_fasjson_client] = get_fasjson_client_override
    return TestClient(main.app)


@pytest.fixture(autouse=True)
def clear_settings(tmp_path):
    with mock.patch(
        "fmn.core.cli.DEFAULT_CONFIG_FILE", new=str(tmp_path / "non-existing-file")
    ), mock.patch("fmn.core.config.settings_file", new=None):
        get_settings.cache_clear()
        yield
