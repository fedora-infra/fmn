import pytest

from fmn.consumer.tracking_rule import (
    ArtifactsFollowed,
    ArtifactsGroupOwned,
    ArtifactsOwned,
    TrackingRule,
)
from fmn.database.model import Rule as RuleRecord
from fmn.database.model import TrackingRule as TrackingRuleRecord


def test_from_record(requester):
    record = RuleRecord(
        tracking_rule=TrackingRuleRecord(name="artifacts-owned", params={"username": "dummy"})
    )
    tr = TrackingRule.from_rule_record(record, requester)
    assert isinstance(tr, ArtifactsOwned)
    assert tr.username == "dummy"

    record = RuleRecord(
        tracking_rule=TrackingRuleRecord(name="artifacts-group-owned", params={"username": "dummy"})
    )
    tr = TrackingRule.from_rule_record(record, requester)
    assert isinstance(tr, ArtifactsGroupOwned)
    assert tr.username == "dummy"

    record = RuleRecord(
        tracking_rule=TrackingRuleRecord(
            name="artifacts-followed", params=[{"name": "dummy", "type": "package"}]
        )
    )
    tr = TrackingRule.from_rule_record(record, requester)
    assert isinstance(tr, ArtifactsFollowed)
    assert tr.followed["packages"] == {"dummy"}

    record = RuleRecord(tracking_rule=TrackingRuleRecord(name="unknown"))
    with pytest.raises(ValueError):
        tr = TrackingRule.from_rule_record(record, requester)
