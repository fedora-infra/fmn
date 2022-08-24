class Notification:
    destination: str
    content: dict

    def __init__(self, destination: str, content):
        self.destination = destination
        self.content = content

    def to_json(self):
        return {
            "destination": self.destination,
            "content": self.content,
        }
