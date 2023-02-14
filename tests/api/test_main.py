from unittest import mock

from fmn.api import main


def test_add_middlewares():
    mw = main.app.user_middleware
    assert len(mw) == 2
    assert mw[0].cls == main.CORSMiddleware
    assert mw[0].options == dict(
        allow_origins=["https://notifications.fedoraproject.org"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    assert mw[1].cls == main.ServerErrorMiddleware
    assert mw[1].options == dict(handler=main.global_execution_handler)


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
