import logging

from fedora_messaging.message import Message
from sqlalchemy import select

from fmn.database.model import Rule as RuleRecord

from .generation_rule import GenerationRule
from .tracking_rule import TrackingRule

log = logging.getLogger(__name__)


class Rule:
    def __init__(
        self,
        id: int,
        username: str,
        tracking_rule: TrackingRule,
        generation_rules: list[GenerationRule],
    ):
        self.id = id
        self.username = username
        self.tracking_rule = tracking_rule
        self.generation_rules = generation_rules

    @classmethod
    def collect(cls, db, requester) -> list[RuleRecord]:
        # Cache this for a reasonable amount of minutes.
        # Rules in the DB could have a last_updated timestamp to rebuild the cache asynchronously
        rules = []
        query = select(RuleRecord)
        for rule_record in db.scalars(query):
            tracking_rule = TrackingRule.from_rule_record(rule_record, requester)
            generation_rules = [
                GenerationRule.from_record(gr, requester) for gr in rule_record.generation_rules
            ]
            rules.append(
                cls(
                    id=rule_record.id,
                    username=rule_record.user.name,
                    tracking_rule=tracking_rule,
                    generation_rules=generation_rules,
                )
            )
        return rules

    def handle(self, message: Message):
        log.debug(f"Rule {self.id} handling message {message.id}")
        if not self.tracking_rule.matches(message):
            log.debug(f"Tracking rule {self.tracking_rule.name} did not match with {message.id}")
            return
        for generation_rule in self.generation_rules:
            yield from generation_rule.handle(message)
