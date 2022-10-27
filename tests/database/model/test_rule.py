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

    async def test_select_related(self, db_async_session, db_async_obj):
        rule = (await db_async_session.execute(model.Rule.select_related())).scalar_one()

        assert rule.user.name == "allkneelbeforezod"
        assert rule.tracking_rule.name == "datrackingrule"
        assert len(rule.generation_rules) == 1
        assert all(isinstance(gr, model.GenerationRule) for gr in rule.generation_rules)

    def test_handle_match(db_async_session, db_async_obj, mocker, make_mocked_message):
        message = make_mocked_message(topic="dummy", body={"foo": "bar"})
        tr = model.TrackingRule(name="dummy")
        tr_matches = mocker.patch.object(tr, "matches", return_value=True)
        gr = model.GenerationRule()
        gr_handle = mocker.patch.object(gr, "handle", return_value=["n1", "n2", "n3"])
        db_async_obj.user = model.User(name="dummy")
        db_async_obj.tracking_rule = tr
        db_async_obj.generation_rules = [gr]
        requester = Mock()
        result = list(db_async_obj.handle(message, requester))
        tr_matches.assert_called_once_with(message, requester)
        gr_handle.assert_called_once_with(message, requester)
        assert result == ["n1", "n2", "n3"]

    def test_handle_no_match(db_async_session, db_async_obj, mocker, make_mocked_message):
        message = make_mocked_message(topic="dummy", body={"foo": "bar"})
        tr = model.TrackingRule(name="dummy")
        tr_matches = mocker.patch.object(tr, "matches", return_value=False)
        gr = model.GenerationRule()
        gr_handle = mocker.patch.object(gr, "handle")
        db_async_obj.user = model.User(name="dummy")
        db_async_obj.tracking_rule = tr
        db_async_obj.generation_rules = [gr]
        requester = Mock()
        result = list(db_async_obj.handle(message, requester))
        tr_matches.assert_called_once_with(message, requester)
        gr_handle.assert_not_called()
        assert len(result) == 0
