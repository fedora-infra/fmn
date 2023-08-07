# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.model import Rule, User
from ...messages.rule import RuleUpdateV1
from .. import api_models
from ..auth import Identity, get_identity_admin
from ..database import gen_db_session
from ..messaging import publish

log = logging.getLogger(__name__)

router = APIRouter(prefix="/admin")


@router.get("/rules", response_model=list[api_models.Rule], tags=["users/rules"])
async def get_rules(
    disabled: bool | None = None,
    username: str | None = None,
    identity: Identity = Depends(get_identity_admin),
    db_session: AsyncSession = Depends(gen_db_session),
):
    query = Rule.select_related()
    if disabled is not None:
        query = query.filter_by(disabled=disabled)

    if username is not None:
        query = query.filter(Rule.user.has(name=username))

    query = query.order_by(Rule.id)
    db_result = await db_session.execute(query)
    return db_result.scalars().all()


@router.get("/users", response_model=list[api_models.User], tags=["users/rules"])
async def get_users(
    search: str | None = None,
    identity: Identity = Depends(get_identity_admin),
    db_session: AsyncSession = Depends(gen_db_session),
):
    query = select(User)

    if search is not None:
        query = query.where(User.name.contains(search))

    db_result = await db_session.execute(query)
    return db_result.scalars().all()


@router.patch("/rules/{id}", response_model=api_models.Rule, tags=["users/rules"])
async def patch_rule(
    id: int,
    rule: api_models.RulePatch,
    identity: Identity = Depends(get_identity_admin),
    db_session: AsyncSession = Depends(gen_db_session),
):
    rule_db = (await db_session.execute(Rule.select_related().filter(Rule.id == id))).scalar()

    if not rule_db:
        raise HTTPException(status_code=404, detail=f"Rule with ID: {id} not found")

    if rule.disabled is not None:
        rule_db.disabled = rule.disabled

    await db_session.commit()

    message = RuleUpdateV1(
        body={
            "rule": api_models.Rule.model_validate(rule_db).model_dump(),
            "user": api_models.User.model_validate(rule_db.user).model_dump(),
        }
    )
    await publish(message)

    return rule_db
