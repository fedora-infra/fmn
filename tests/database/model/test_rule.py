# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest.mock import Mock

from fmn.database import model

from .base import ModelTestBase


class TestRule(ModelTestBase):
    cls = model.Rule

    attrs = {
        "name": "darule",
    }

    def _db_obj_get_dependencies(self):
        return {
            "user": model.User(name="allkneelbeforezod"),
            "tracking_rule": model.TrackingRule(name="datrackingrule"),
            "generation_rules": [model.GenerationRule()],
        }

    async def test_select_related(self, db_async_session, db_obj):
        rule = (await db_async_session.execute(model.Rule.select_related())).scalar_one()

        assert rule.user.name == "allkneelbeforezod"
        assert rule.tracking_rule.name == "datrackingrule"
        assert len(rule.generation_rules) == 1
        assert all(isinstance(gr, model.GenerationRule) for gr in rule.generation_rules)

    async def test_handle_match(self, db_async_session, db_obj, mocker, make_mocked_message):
        message = make_mocked_message(topic="dummy", body={"foo": "bar"})
        tr = db_obj.tracking_rule
        # tr = model.TrackingRule(name="dummy", rule_id=db_obj.id)
        tr_matches = mocker.patch.object(tr, "matches", return_value=True)
        # gr = model.GenerationRule()
        # db_obj.user = model.User(name="dummy")
        # db_obj.tracking_rule = tr
        # db_obj.generation_rules = [gr]
        gr = db_obj.generation_rules[0]
        for i in range(1, 4):
            db_async_session.add(
                model.Destination(protocol="email", address=f"n{i}", generation_rule=gr)
            )
        await db_async_session.flush()
        requester = Mock()
        rule_result = await db_async_session.execute(
            db_obj.select_related().filter_by(id=db_obj.id)
        )
        result = [n async for n in rule_result.scalar_one().handle(message, requester)]
        tr_matches.assert_called_once_with(message, requester)
        assert len(result) == 3
        assert [n.content.headers.model_dump()["To"] for n in result] == ["n1", "n2", "n3"]

    async def test_handle_no_match(db_async_session, db_obj, mocker, make_mocked_message):
        message = make_mocked_message(topic="dummy", body={"foo": "bar"})
        tr = model.TrackingRule(name="dummy")
        tr_matches = mocker.patch.object(tr, "matches", return_value=False)
        gr = model.GenerationRule()
        gr_handle = mocker.patch.object(gr, "handle")
        db_obj.user = model.User(name="dummy")
        db_obj.tracking_rule = tr
        db_obj.generation_rules = [gr]
        requester = Mock()
        result = [n async for n in db_obj.handle(message, requester)]
        tr_matches.assert_called_once_with(message, requester)
        gr_handle.assert_not_called()
        assert len(result) == 0
