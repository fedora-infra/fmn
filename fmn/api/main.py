# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.requests import Request as StarletteRequest
from starlette.types import ASGIApp

from ..cache import configure_cache
from ..core.config import get_settings
from . import handlers
from .database import get_manager

log = logging.getLogger(__name__)

tags_metadata = [
    {"name": "users", "description": "Work with users"},
    {"name": "users/rules", "description": "Work with users’ rules"},
    {"name": "misc", "description": "Miscellaneous"},
]

app = FastAPI(title="Fedora Messaging Notifications", openapi_tags=tags_metadata)


# API v1

PREFIX = "/api/v1"

app.include_router(handlers.users.router, prefix=PREFIX)
app.include_router(handlers.misc.router, prefix=PREFIX)
app.include_router(handlers.admin.router, prefix=PREFIX)

# Setup of middleware and database access


async def global_execution_handler(
    request: StarletteRequest, exc: Exception
) -> ASGIApp:  # pragma: no cover todo
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content="Unknown Error",
    )


app.add_middleware(
    ServerErrorMiddleware,
    handler=global_execution_handler,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins.split(" "),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def configure_cache_on_startup():
    db_manager = get_manager()
    configure_cache(db_manager=db_manager)
