from functools import cache as ft_cache
from functools import partial
from typing import Any, Callable

from cashews import cache

from ..core import config


def configure_cache(**kwargs):
    settings = config.get_settings()
    args = (settings.cache.setup_args or {}) | kwargs
    cache.setup(settings.cache.url, **args)


@ft_cache
def cache_arg(arg: str, scope: str | None = None) -> Callable[[str, str | None], Any]:
    """Generate a cached function for cashews decorator arguments.

    The purpose of this is to evaluate the settings late (i.e. the first time
    a decorated callable is called), so customized settings can be applied
    effectively."""

    @ft_cache
    def get_cache_arg(*cached_fn_args, **cached_fn_kwargs) -> Any:
        f"""Get the cache arg {arg} for scope {scope}."""
        settings = config.get_settings()

        if scope:
            try:
                return getattr(settings.cache.scoped_args[scope], arg)
            except (AttributeError, KeyError):
                pass

        return getattr(settings.cache.default_args, arg)

    return get_cache_arg


cache_ttl = partial(cache_arg, "ttl")
