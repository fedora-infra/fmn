from fmn.database import model

from .base import ModelTestBase


class TestUser(ModelTestBase):
    cls = model.User
    attrs = {
        "name": "beefymiracle",
    }
