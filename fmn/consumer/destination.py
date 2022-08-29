from fedora_messaging.message import Message


class Destination:

    name: str
    address: str

    def __init__(self, address):
        self.address = address

    @classmethod
    def from_rule(cls, rule: "RuleRecord"):  # noqa
        def get_class(address):
            for subclass in cls.__subclasses__:
                if address.startswith(f"{subclass.name}:"):
                    return subclass

        destinations = []
        for address in rule.destination:
            subclass = get_class(address)
            destinations.append(subclass(address))
        return destinations

    def generate(self, message: Message):
        raise NotImplementedError


class Email(Destination):
    name = "email"

    def generate(self, message):
        return {
            "headers": {
                "To": self.address,
                "Subject": message.subject,
            },
            "body": str(message),
        }


class IRC(Destination):
    name = "irc"

    def generate(self, message):
        return {
            "to": self.address,
            "message": message.subject,
        }
