# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from fmn.api import main

EXPECTED_MIDDLEWARES = [
    (
        main.CORSMiddleware,
        {
            "allow_origins": ["https://notifications.fedoraproject.org"],
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        },
    ),
    (main.ServerErrorMiddleware, {"handler": main.global_execution_handler}),
]


def test_add_middlewares():
    for mw, (exp_cls, exp_kwargs) in zip(
        main.app.user_middleware, EXPECTED_MIDDLEWARES, strict=True
    ):
        # Middlewares in starlette < 0.35 only have `.options`, >= 0.35 they have `.args` and
        # `.kwargs`. Casting the middleware into a tuple (via iter()) allows coping with both
        # variants.
        mwinfo = tuple(mw)
        cls = mwinfo[0]
        kwargs = mwinfo[-1]
        assert cls == exp_cls
        assert kwargs == exp_kwargs


def test_configure_cache(mocker):
    configure_cache = mocker.patch("fmn.api.main.configure_cache")
    assert main.configure_cache_on_startup in main.app.router.on_startup
    main.configure_cache_on_startup()
    configure_cache.assert_called_once()
