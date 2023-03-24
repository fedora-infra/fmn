from fmn.cache.tracked import TrackedCache
from fmn.core.cli import cli


def test_get_tracked(mocker, cli_runner, mocked_fasjson_proxy):
    configure_cache = mocker.patch("fmn.cache.cli.configure_cache")
    get_value = mocker.patch.object(TrackedCache, "get_value")
    get_value.return_value = {"foo": "bar"}
    mocker.patch("fmn.cache.cli.init_async_model")

    result = cli_runner.invoke(cli, ["cache", "get-tracked"])

    assert result.exit_code == 0, result.output
    configure_cache.assert_called_once_with()
    get_value.assert_called_once()
    assert result.output == "{'foo': 'bar'}\n"


def test_delete_tracked(mocker, cli_runner):
    configure_cache = mocker.patch("fmn.cache.cli.configure_cache")
    get_value = mocker.patch.object(TrackedCache, "get_value")
    get_value.return_value = {"foo": "bar"}
    invalidate_tracked = mocker.patch.object(TrackedCache, "invalidate")

    result = cli_runner.invoke(cli, ["cache", "delete-tracked"])

    assert result.exit_code == 0, result.output
    configure_cache.assert_called_once_with()
    invalidate_tracked.assert_called_once_with()
