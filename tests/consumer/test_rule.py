from unittest.mock import Mock

import pytest

from fmn.consumer.rule import Rule
from fmn.database.main import get_sync_engine, init_sync_model, metadata, sync_session_maker
from fmn.database.model import Destination as DestinationRecord
from fmn.database.model import Filter as FilterRecord
from fmn.database.model import GenerationRule as GenerationRuleRecord
from fmn.database.model import Rule as RuleRecord
from fmn.database.model import TrackingRule as TrackingRuleRecord
from fmn.database.model import User as UserRecord
from fmn.database.setup import setup_db_schema

from .conftest import Message


@pytest.fixture()
def db_session():
    engine = get_sync_engine()
    setup_db_schema(engine=engine)
    init_sync_model(sync_engine=engine)
    session = sync_session_maker()
    yield session
    metadata.drop_all(bind=engine)


def test_collect(db_session):
    requester = Mock()
    user = UserRecord(name="dummy")
    record = RuleRecord(user=user, name="the name")
    tr = TrackingRuleRecord(rule=record, name="artifacts-owned", params={"username": "dummy"})
    gr = GenerationRuleRecord(rule=record)
    f = FilterRecord(generation_rule=gr, name="not_my_actions")
    d = DestinationRecord(generation_rule=gr, protocol="email", address="dummy@example.com")
    db_session.add_all([user, record, tr, gr, f, d])
    db_session.commit()

    result = Rule.collect(db_session, requester)

    assert len(result) == 1
    rule = result[0]
    assert rule.username == "dummy"
    assert rule.tracking_rule.name == "artifacts-owned"
    assert rule.tracking_rule._params == {"username": "dummy"}
    assert len(rule.generation_rules) == 1
    gr = rule.generation_rules[0]
    assert len(gr.filters) == 1
    assert gr.filters[0].name == "not_my_actions"
    assert len(gr.destinations) == 1
    assert gr.destinations[0].protocol == "email"
    assert gr.destinations[0].address == "dummy@example.com"


def test_handle_match():
    message = Message(topic="dummy", body={"foo": "bar"})
    tr = Mock()
    tr.matches.return_value = True
    gr = Mock()
    gr.handle.return_value = ["n1", "n2", "n3"]
    rule = Rule(id=1, username="dummy", tracking_rule=tr, generation_rules=[gr])
    result = list(rule.handle(message))
    tr.matches.assert_called_once_with(message)
    gr.handle.assert_called_once_with(message)
    assert result == ["n1", "n2", "n3"]


def test_handle_no_match():
    message = Message(topic="dummy", body={"foo": "bar"})
    tr = Mock()
    tr.matches.return_value = False
    gr = Mock()
    rule = Rule(id=1, username="dummy", tracking_rule=tr, generation_rules=[gr])
    result = list(rule.handle(message))
    tr.matches.assert_called_once_with(message)
    gr.handle.assert_not_called()
    assert len(result) == 0
