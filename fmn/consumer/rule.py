from fedora_messaging.message import Message

from .filter import Filter
from .notification import Notification
from .tracking_rule import TrackingRule


class Rule:
    def __init__(self, id: int, username: str, tracking_rule: TrackingRule, filters: list[Filter]):
        self.id = id
        self.username = username
        self.tracking_rule = tracking_rule
        self.filters = filters

    @classmethod
    def collect(cls, db, requester):
        # Cache this for a reasonable amount of minutes.
        # Rules in the DB could have a last_updated timestamp to rebuild the cache asynchronously
        rules = []
        for rule_record in db.get_rules():
            tracking_rule = TrackingRule.from_rule(rule_record, requester)
            filters = Filter.from_rule(rule_record, requester)
            rules.append(
                cls(
                    id=rule_record.id,
                    username=rule_record.username,
                    tracking_rule=tracking_rule,
                    filters=filters,
                )
            )
        return rules

    def handle(self, message: Message):
        if not self.tracking_rule.matches(message):
            return []
        notifications = []
        for filter in self.filters:
            if not filter.matches(message):
                continue
            for destination in filter.destinations:
                notifications.append(
                    Notification(
                        destination=destination.name, content=destination.generate(message)
                    )
                )
        return notifications
