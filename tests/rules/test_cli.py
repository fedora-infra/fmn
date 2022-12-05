from fmn.core.cli import cli

# from fmn.rules import cli as rules_cli


def test_get_tracked(mocker, cli_runner, mocked_fasjson_client):
    cache = mocker.patch("fmn.rules.cli.cache")
    mocker.patch("fmn.rules.cli.init_sync_model")
    cache.get_tracked.return_value = {"foo": "bar"}
    result = cli_runner.invoke(cli, ["cache", "get-tracked"])

    assert result.exit_code == 0
    cache.configure.assert_called_once_with()
    cache.get_tracked.assert_called_once()
    assert result.output == "{'foo': 'bar'}\n"


def test_delete_tracked(mocker, cli_runner):
    cache = mocker.patch("fmn.rules.cli.cache")
    cache.get_tracked.return_value = {"foo": "bar"}
    result = cli_runner.invoke(cli, ["cache", "delete-tracked"])

    assert result.exit_code == 0
    cache.configure.assert_called_once_with()
    cache.invalidate_tracked.assert_called_once_with()
