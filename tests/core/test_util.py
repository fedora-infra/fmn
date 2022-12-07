import inspect
from unittest import mock

import pytest

from fmn.core import util


@pytest.mark.parametrize("inside_asyncio", (True, False))
@mock.patch.object(util.asyncio, "new_event_loop")
@mock.patch.object(util.asyncio, "get_event_loop")
def test_acquire_asyncio_event_loop(get_event_loop, new_event_loop, inside_asyncio):
    if inside_asyncio:
        get_event_loop.return_value = get_sentinel = object()
    else:
        get_event_loop.side_effect = RuntimeError()
        new_event_loop.return_value = new_sentinel = object()

    loop = util.acquire_asyncio_event_loop()

    get_event_loop.assert_called_once_with()
    if inside_asyncio:
        assert loop is get_sentinel
        new_event_loop.assert_not_called()
    else:
        assert loop is new_sentinel
        new_event_loop.assert_called_with()


class TestMakeSynchronous:
    class ToBeWrapped:
        async def wrapped_method(self):
            return "wrapped method"

        async def wrapped_iter(self):
            for i in range(4):
                yield f"wrapped iter #{i}"

        def unwrapped_method(self):
            return "unwrapped method"

        class_attribute = "class attribute"

    Wrapped = util.make_synchronous(ToBeWrapped, "Wrapped")

    def test_wrapped_method(self):
        wrapped = self.Wrapped()

        assert inspect.isfunction(self.Wrapped.wrapped_method)
        assert inspect.ismethod(wrapped.wrapped_method)
        assert wrapped.wrapped_method() == "wrapped method"

    def test_wrapped_iter(self):
        wrapped = self.Wrapped()

        assert inspect.isgeneratorfunction(self.Wrapped.wrapped_iter)
        assert inspect.ismethod(wrapped.wrapped_iter)
        assert inspect.isgenerator(wrapped.wrapped_iter())
        assert list(wrapped.wrapped_iter()) == [f"wrapped iter #{i}" for i in range(4)]

    def test_unwrapped_method(self):
        wrapped = self.Wrapped()

        assert wrapped.unwrapped_method() == "unwrapped method"

    def test_read_class_attribute(self):
        wrapped = self.Wrapped()

        assert wrapped.class_attribute == wrapped.__wrapped__.class_attribute

    def test_write_class_attribute(self):
        wrapped = self.Wrapped()

        wrapped.class_attribute = "new attribute"

        assert wrapped.class_attribute == "new attribute"
        assert wrapped.class_attribute == wrapped.__wrapped__.class_attribute

    def test_read_instance_attribute(self):
        wrapped = self.Wrapped()

        wrapped.__wrapped__.instance_attribute = "instance attribute"

        assert wrapped.instance_attribute == "instance attribute"

    def test_write_instance_attribute(self):
        wrapped = self.Wrapped()

        wrapped.instance_attribute = "new attribute"

        assert wrapped.instance_attribute == "new attribute"
        assert wrapped.instance_attribute == wrapped.__wrapped__.instance_attribute
