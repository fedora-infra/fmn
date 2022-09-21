from fedora_messaging.message import Message

from fmn.database.model import Destination as DestinationRecord


class Destination:

    protocol: str
    address: str

    def __init__(self, address):
        self.address = address

    @classmethod
    def from_record(cls, record: DestinationRecord):
        def get_class(protocol):
            for subclass in cls.__subclasses__():
                if subclass.protocol == protocol:
                    return subclass
            raise ValueError(f"No such destination: {protocol}")

        subclass = get_class(record.protocol)
        return subclass(record.address)

    def generate(self, message: Message):
        raise NotImplementedError  # pragma: no cover


class Email(Destination):
    protocol = "email"

    def generate(self, message):
        return {
            "headers": {
                "To": self.address,
                "Subject": message.summary,
            },
            "body": str(message),
        }


class IRC(Destination):
    protocol = "irc"

    def generate(self, message):
        return {
            "to": self.address,
            "message": message.summary,
        }
