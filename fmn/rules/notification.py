from pydantic import BaseModel


class Notification(BaseModel):
    protocol: str
    content: dict
