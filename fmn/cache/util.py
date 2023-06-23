# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from collections.abc import Callable, Iterator
from functools import cache as ft_cache
from functools import partial
from typing import Any

from cashews.formatter import get_templates_for_func, template_to_pattern
from cashews.key import get_func_params

from ..core import config


@ft_cache
def cache_arg(arg: str, scope: str | None = None) -> Callable[[str, str | None], Any]:
    """Generate a cached function for cashews decorator arguments.

    The purpose of this is to evaluate the settings late (i.e. the first time
    a decorated callable is called), so customized settings can be applied
    effectively."""

    @ft_cache
    def get_cache_arg(*cached_fn_args, **cached_fn_kwargs) -> Any:
        settings = config.get_settings()

        if scope:
            try:
                return getattr(getattr(settings.cache.scoped_args, scope), arg)
            except (AttributeError, KeyError):
                pass

        return getattr(settings.cache.default_args, arg)

    return get_cache_arg


cache_ttl = partial(cache_arg, "ttl")
lock_ttl = partial(cache_arg, "lock_ttl")


def _get_pattern_for_cached_calls_iter(func: Callable, **kwargs: dict[str, Any]) -> Iterator[str]:
    # This is taken from cashews.validation.invalidate_func(), minus the actual deletion part. This
    # allows making decisions on the (cached) return values.
    values = {**{param: "*" for param in get_func_params(func)}, **kwargs}
    for template in get_templates_for_func(func):
        yield template_to_pattern(template, **values)


@ft_cache
def get_pattern_for_cached_calls(func: Callable, **kwargs: dict[str, Any]) -> list[str]:
    return list(_get_pattern_for_cached_calls_iter(func, **kwargs))
