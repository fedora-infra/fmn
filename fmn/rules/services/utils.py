import logging
from functools import wraps

import httpx

log = logging.getLogger(__name__)


def handle_http_error(default_factory):
    def exception_handler(f):
        @wraps(f)
        async def wrapper(*args, **kw):
            try:
                return await f(*args, **kw)
            except httpx.HTTPStatusError as e:
                log.warning(f"Request failed: {e}")
                return default_factory()

        return wrapper

    return exception_handler


def normalize_url(url):
    return url.rstrip("/") + "/"
