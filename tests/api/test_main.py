from unittest import mock

from fmn.api import main


@mock.patch("fmn.api.main.get_settings")
@mock.patch("fmn.api.main.app")
def test_add_middlewares(app, get_settings):
    get_settings.return_value = mock.Mock(cors_origins="https://foo")
    main.add_middlewares()

    calls = [
        mock.call(
            main.CORSMiddleware,
            allow_origins=["https://foo"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
    app.add_middleware.assert_has_calls(calls)
    assert app.add_middleware.call_count == 2


@mock.patch("fmn.api.main.init_async_model")
async def test_init_model(init_async_model):
    assert main.init_model in main.app.router.on_startup

    await main.init_model()

    init_async_model.assert_awaited_once_with()


def test_configure_cache(mocker):
    configure_cache = mocker.patch("fmn.api.main.configure_cache")
    assert main.configure_cache_on_startup in main.app.router.on_startup
    main.configure_cache_on_startup()
    configure_cache.assert_called_once_with()
