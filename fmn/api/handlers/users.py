# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from datetime import datetime, timedelta
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from ...backends import FASJSONAsyncProxy, get_fasjson_proxy
from ...core.constants import DEFAULT_MATRIX_DOMAIN
from ...database.model import Destination, Filter, Generated, GenerationRule, Rule, User
from ...messages.rule import RuleCreateV1, RuleDeleteV1, RuleUpdateV1
from .. import api_models
from ..auth import Identity, get_identity, get_identity_optional
from ..database import gen_db_session
from ..messaging import publish
from .utils import db_rule_from_api_rule

log = logging.getLogger(__name__)

router = APIRouter(prefix="/users")


@router.get("/me", response_model=api_models.User, tags=["users"])
async def get_me(
    identity: Identity = Depends(get_identity),
    db_session: AsyncSession = Depends(gen_db_session),
):
    user, created = await User.get_or_create(db_session, name=identity.name)
    user.is_admin = identity.admin
    return user


@router.get("", response_model=list[str], tags=["users"])
async def get_users(
    search: str | None = None,
    identity: Identity = Depends(get_identity_optional),
    fasjson_proxy: FASJSONAsyncProxy = Depends(get_fasjson_proxy),
):
    if not search:
        if identity and identity.name:
            return [identity.name]
        else:
            return []
    return [u["username"] for u in await fasjson_proxy.search_users(username=search)]


@router.get("/{username}/info", tags=["users"])
async def get_user_info(username, fasjson_proxy: FASJSONAsyncProxy = Depends(get_fasjson_proxy)):
    return await fasjson_proxy.get_user(username=username)


@router.get("/{username}/groups", response_model=list[str], tags=["users"])
async def get_user_groups(username, fasjson_proxy: FASJSONAsyncProxy = Depends(get_fasjson_proxy)):
    return [g["groupname"] for g in await fasjson_proxy.get_user_groups(username=username)]


@router.get("/{username}/destinations", response_model=list[api_models.Destination], tags=["users"])
async def get_user_destinations(
    username, fasjson_proxy: FASJSONAsyncProxy = Depends(get_fasjson_proxy)
):
    user = await fasjson_proxy.get_user(username=username)
    result = [{"protocol": "email", "address": email} for email in user["emails"]]
    nicks = user.get("ircnicks") or []
    for nick in nicks:
        url = urlparse(nick)
        address = url.path.lstrip("/")
        protocol = url.scheme
        if not protocol:
            protocol = "irc"
        if protocol == "matrix":
            domain = url.hostname or DEFAULT_MATRIX_DOMAIN
            address = f"@{address}:{domain}"
        result.append({"protocol": protocol, "address": address})
    return result


@router.get("/{username}/rules", response_model=list[api_models.Rule], tags=["users/rules"])
async def get_user_rules(
    username,
    identity: Identity = Depends(get_identity),
    db_session: AsyncSession = Depends(gen_db_session),
):
    if username != identity.name:
        raise HTTPException(status_code=403, detail="Not allowed to see someone else's rules")

    db_result = await db_session.execute(
        Rule.select_related().filter(Rule.user.has(name=username)).order_by(Rule.id)
    )
    rules = db_result.scalars().all()

    # Collect the number of notifications sent
    last_week = datetime.now() - timedelta(days=7)
    db_result = await db_session.execute(
        select(Rule.id, func.sum(Generated.count))
        .join(Rule)
        .group_by(Rule)
        .filter(Rule.id.in_([r.id for r in rules]))
        .filter(Generated.when >= last_week)
    )
    counts = dict(db_result.all())
    for rule in rules:
        rule.generated_last_week = counts.get(rule.id, 0)
    return rules


@router.get("/{username}/rules/{id}", response_model=api_models.Rule, tags=["users/rules"])
async def get_user_rule(
    username: str,
    id: int,
    identity: Identity = Depends(get_identity),
    db_session: AsyncSession = Depends(gen_db_session),
):
    if username != identity.name:
        raise HTTPException(status_code=403, detail="Not allowed to see someone else's rules")

    try:
        return (
            await db_session.execute(
                Rule.select_related().filter(Rule.id == id, Rule.user.has(name=username))
            )
        ).scalar_one()
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=f"No rule with ID {id}.") from e


@router.put("/{username}/rules/{id}", response_model=api_models.Rule, tags=["users/rules"])
async def edit_user_rule(
    username: str,
    id: int,
    rule: api_models.Rule,
    identity: Identity = Depends(get_identity),
    db_session: AsyncSession = Depends(gen_db_session),
):
    if username != identity.name:
        raise HTTPException(status_code=403, detail="Not allowed to edit someone else's rules")

    rule_db = (
        await db_session.execute(
            Rule.select_related().filter(Rule.id == id, Rule.user.has(name=username))
        )
    ).scalar_one()
    rule_db.name = rule.name
    rule_db.disabled = rule.disabled
    rule_db.tracking_rule.name = rule.tracking_rule.name
    rule_db.tracking_rule.params = rule.tracking_rule.params
    for to_delete in rule_db.generation_rules[len(rule.generation_rules) :]:
        await db_session.delete(to_delete)
    for index, gr in enumerate(rule.generation_rules):
        try:
            gr_db = rule_db.generation_rules[index]
        except IndexError:
            gr_db = GenerationRule(rule=rule_db)
            rule_db.generation_rules.append(gr_db)
        for to_delete in gr_db.destinations[len(gr.destinations) :]:
            await db_session.delete(to_delete)
        for index, dst in enumerate(gr.destinations):
            try:
                dst_db = gr_db.destinations[index]
            except IndexError:
                dst_db = Destination(
                    generation_rule=gr_db, protocol=dst.protocol, address=dst.address
                )
                gr_db.destinations.append(dst_db)
            else:
                dst_db.protocol = dst.protocol
                dst_db.address = dst.address
        to_delete = [
            f for f in gr_db.filters if f.name not in gr.filters.model_dump(exclude_unset=True)
        ]
        for f in to_delete:
            await db_session.delete(f)
        existing_filters = {f.name: f for f in gr_db.filters}
        for f_name, f_params in gr.filters.model_dump(exclude_unset=True).items():
            try:
                f_db = existing_filters[f_name]
            except KeyError:
                f_db = Filter(generation_rule=gr_db, name=f_name, params=f_params)
                gr_db.filters.append(f_db)
            else:
                f_db.name = f_name
                f_db.params = f_params
        await db_session.flush()
    await db_session.commit()

    # Refresh using the full query to get relationships
    db_session.expire(rule_db)
    rule_db = (
        await db_session.execute(
            Rule.select_related().filter(Rule.id == id, Rule.user.has(name=username))
        )
    ).scalar_one()

    message = RuleUpdateV1(
        body={
            "rule": api_models.Rule.model_validate(rule_db).model_dump(),
            "user": api_models.User.model_validate(rule_db.user).model_dump(),
        }
    )
    await publish(message)

    return rule_db


@router.delete("/{username}/rules/{id}", tags=["users/rules"])
async def delete_user_rule(
    username: str,
    id: int,
    identity: Identity = Depends(get_identity),
    db_session: AsyncSession = Depends(gen_db_session),
):
    if username != identity.name:
        raise HTTPException(status_code=403, detail="Not allowed to delete someone else's rules")

    # We need the full query to populate the outgoing message
    rule = (
        await db_session.execute(
            Rule.select_related().filter(Rule.id == id, Rule.user.has(name=username))
        )
    ).scalar_one()

    message = RuleDeleteV1(
        body={
            "rule": api_models.Rule.model_validate(rule).model_dump(),
            "user": api_models.User.model_validate(rule.user).model_dump(),
        }
    )

    await db_session.delete(rule)
    await db_session.commit()
    await publish(message)


@router.post("/{username}/rules", response_model=api_models.Rule, tags=["users/rules"])
async def create_user_rule(
    username,
    rule: api_models.NewRule,
    identity: Identity = Depends(get_identity),
    db_session: AsyncSession = Depends(gen_db_session),
):
    if username != identity.name:
        raise HTTPException(status_code=403, detail="Not allowed to edit someone else's rules")
    log.info("Creating rule: %s", rule)
    user = await User.get_one(db_session, name=username)
    rule_db = db_rule_from_api_rule(rule, user)
    db_session.add(rule_db)
    await db_session.commit()

    # Refresh using the full query to get relationships
    rule_db = (
        await db_session.execute(
            Rule.select_related().filter(Rule.id == rule_db.id, Rule.user.has(name=username))
        )
    ).scalar_one()

    message = RuleCreateV1(
        body={
            "rule": api_models.Rule.model_validate(rule_db).model_dump(),
            "user": api_models.User.model_validate(rule_db.user).model_dump(),
        }
    )
    await publish(message)

    return rule_db
