from fedora_messaging.message import Message

from fmn.database.model import GenerationRule as GenerationRuleRecord

from .destination import Destination
from .filter import Filter
from .notification import Notification
from .requester import Requester


class GenerationRule:

    destinations: list[Destination]
    filters: list[Filter]

    def __init__(self, destinations, filters):
        self.destinations = destinations
        self.filters = filters

    @classmethod
    def from_record(cls, record: "GenerationRuleRecord", requester: Requester):
        destinations = [Destination.from_record(d) for d in record.destinations]
        filters = [Filter.from_record(f, requester) for f in record.filters]
        return cls(destinations, filters)

    def handle(self, message: Message):
        if self.filters and not all([f.matches(message) for f in self.filters]):
            return
        for destination in self.destinations:
            yield Notification(protocol=destination.protocol, content=destination.generate(message))
