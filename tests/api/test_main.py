from fmn.api import main


def test_read_root():
    assert main.read_root()["Hello"] == "World"
