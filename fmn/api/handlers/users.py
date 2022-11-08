import logging

from fasjson_client import Client as FasjsonClient
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.model import Destination, Filter, GenerationRule, Rule, User
from .. import api_models
from ..auth import Identity, get_identity, get_identity_optional
from ..database import gen_db_session
from ..fasjson import get_fasjson_client
from .utils import db_rule_from_api_rule

log = logging.getLogger(__name__)

router = APIRouter(prefix="/users")


@router.get("", response_model=list[str], tags=["users"])
async def get_users(
    search: str,
    identity: Identity = Depends(get_identity_optional),
    fasjson_client: FasjsonClient = Depends(get_fasjson_client),
):  # pragma: no cover todo
    if not search:
        if identity and identity.name:
            return [identity.name]
        else:
            return []
    return [u["username"] for u in fasjson_client.search(username=search).result]


@router.get("/{username}", response_model=api_models.User, tags=["users"])
async def get_user(username, db_session: AsyncSession = Depends(gen_db_session)):
    user = await User.async_get_or_create(db_session, name=username)
    return user


@router.get("/{username}/info", tags=["users"])
def get_user_info(
    username, fasjson_client: FasjsonClient = Depends(get_fasjson_client)
):  # pragma: no cover todo
    return fasjson_client.get_user(username=username).result


@router.get("/{username}/groups", tags=["users"])
def get_user_groups(username, fasjson_client: FasjsonClient = Depends(get_fasjson_client)):
    return [g["groupname"] for g in fasjson_client.list_user_groups(username=username).result]


@router.get("/{username}/destinations", response_model=list[api_models.Destination], tags=["users"])
def get_user_destinations(
    username, fasjson_client: FasjsonClient = Depends(get_fasjson_client)
):  # pragma: no cover todo
    user = fasjson_client.get_user(username=username).result
    result = [{"protocol": "email", "address": email} for email in user["emails"]]
    for nick in user.get("ircnicks", []):
        address = nick.split(":", 1)[1] if ":" in nick else nick
        if nick.startswith("matrix:"):
            protocol = "matrix"
        else:
            protocol = "irc"
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

    db_result = await db_session.execute(Rule.select_related().filter(Rule.user.has(name=username)))
    return db_result.scalars().all()


@router.get("/{username}/rules/{id}", response_model=api_models.Rule, tags=["users/rules"])
async def get_user_rule(
    username: str,
    id: int,
    identity: Identity = Depends(get_identity),
    db_session: AsyncSession = Depends(gen_db_session),
):
    if username != identity.name:
        raise HTTPException(status_code=403, detail="Not allowed to see someone else's rules")

    return (
        await db_session.execute(
            Rule.select_related().filter(Rule.id == id, Rule.user.has(name=username))
        )
    ).scalar_one()


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
        to_delete = [f for f in gr_db.filters if f.name not in gr.filters.dict(exclude_unset=True)]
        for f in to_delete:
            await db_session.delete(f)
        existing_filters = {f.name: f for f in gr_db.filters}
        for f_name, f_params in gr.filters.dict(exclude_unset=True).items():
            try:
                f_db = existing_filters[f_name]
            except KeyError:
                f_db = Filter(generation_rule=gr_db, name=f_name, params=f_params)
                gr_db.filters.append(f_db)
            else:
                f_db.name = f_name
                f_db.params = f_params
        await db_session.flush()

    # TODO: emit a fedmsg

    # Refresh using the full query to get relationships
    return (
        await db_session.execute(
            Rule.select_related().filter(Rule.id == id, Rule.user.has(name=username))
        )
    ).scalar_one()


@router.delete("/{username}/rules/{id}", tags=["users/rules"])
async def delete_user_rule(
    username: str,
    id: int,
    identity: Identity = Depends(get_identity),
    db_session: AsyncSession = Depends(gen_db_session),
):
    if username != identity.name:
        raise HTTPException(status_code=403, detail="Not allowed to delete someone else's rules")

    rule = await Rule.async_get(db_session, id=id)
    await db_session.delete(rule)
    await db_session.flush()

    # TODO: emit a fedmsg


@router.post("/{username}/rules", response_model=api_models.Rule, tags=["users/rules"])
async def create_user_rule(
    username,
    rule: api_models.Rule,
    identity: Identity = Depends(get_identity),
    db_session: AsyncSession = Depends(gen_db_session),
):
    if username != identity.name:
        raise HTTPException(status_code=403, detail="Not allowed to edit someone else's rules")
    log.info("Creating rule:", rule)
    user = await User.async_get_or_create(db_session, name=username)
    rule_db = db_rule_from_api_rule(rule, user)
    db_session.add(rule_db)
    await db_session.flush()

    # TODO: emit a fedmsg

    # Refresh using the full query to get relationships
    return (
        await db_session.execute(
            Rule.select_related().filter(Rule.id == rule_db.id, Rule.user.has(name=username))
        )
    ).scalar_one()
