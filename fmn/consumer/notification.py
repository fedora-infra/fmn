class Notification:
    protocol: str
    content: dict

    def __init__(self, protocol: str, content):
        self.protocol = protocol
        self.content = content

    def to_json(self):
        return {
            "protocol": self.protocol,
            "content": self.content,
        }
