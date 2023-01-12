from cashews import cache

from ..core import config


def configure_cache(**kwargs):
    settings = config.get_settings()
    args = settings.cache.arguments or {}
    args.update(kwargs)
    cache.setup(settings.cache.url, **args)
