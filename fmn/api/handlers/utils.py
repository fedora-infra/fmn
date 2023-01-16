from typing import Iterator

from fedora_messaging import message

from fmn.backends import DatagrepperAsyncProxy
from fmn.core.config import get_settings
from fmn.database.model import Destination, Filter, GenerationRule, Rule, TrackingRule
from fmn.rules.requester import Requester


def db_rule_from_api_rule(rule, user):
    rule_db = Rule(user=user, name=rule.name, disabled=rule.disabled)
    rule_db.tracking_rule = TrackingRule(
        name=rule.tracking_rule.name, params=rule.tracking_rule.params
    )
    for generation_rule in rule.generation_rules:
        gr = GenerationRule(rule=rule_db)
        for destination in generation_rule.destinations:
            gr.destinations.append(
                Destination(protocol=destination.protocol, address=destination.address)
            )
        for name, params in generation_rule.filters.dict().items():
            gr.filters.append(Filter(name=name, params=params))
    return rule_db


def gen_requester() -> Iterator[Requester]:
    """Generate a rule Requester for FastAPI request handlers.

    This lets users declare the requester as a dependency in request handler
    functions..

    :return: A :class:`fmn.rules.requester.Requester` object for the
        current request
    """
    requester = Requester(get_settings().services)
    yield requester


# TODO: absolutely cache this
async def get_last_messages(hours):
    proxy = DatagrepperAsyncProxy(get_settings().services.datagrepper_url)

    async for msg_dict in proxy.search(delta=int(hours) * 60 * 60, rows_per_page=100):
        yield get_message(msg_dict)


# Replace this with fedora_messaging.message.load_message() when it's published.
def get_message(message_dict):  # pragma: no cover
    MessageClass = message.get_class(
        message_dict["headers"].get("fedora_messaging_schema", "base.message")
    )
    # The headers dict is altered by the Message constructor! :-(
    headers = message_dict["headers"].copy()
    msg = MessageClass(
        body=message_dict["body"],
        topic=message_dict["topic"],
        headers=message_dict["headers"],
        severity=message_dict["headers"].get("fedora_messaging_severity"),
    )
    msg.queue = message_dict["queue"] if "queue" in message_dict else None
    msg.id = message_dict["id"]
    msg.priority = message_dict.get("priority")
    if "sent-at" in headers:
        msg._headers["sent-at"] = headers["sent-at"]
    return msg
