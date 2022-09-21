class Notification:
    protocol: str
    content: dict

    def __init__(self, protocol: str, content):
        self.protocol = protocol
        self.content = content
