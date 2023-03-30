# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest import mock

import pytest
from fedora_messaging import exceptions as fm_exceptions

from fmn.api import messaging
from fmn.messages.rule import RuleCreateV1


def test__publish(mocker):
    api_publish = mocker.patch("fedora_messaging.api.publish")
    messaging._publish(RuleCreateV1({"rule": {}, "user": {}}))
    api_publish.assert_called_once()


def test__publish_with_errors(mocker):
    api_publish = mocker.patch("fedora_messaging.api.publish")
    api_publish.side_effect = fm_exceptions.ConnectionException()
    with pytest.raises(fm_exceptions.ConnectionException):
        messaging._publish(RuleCreateV1({"rule": {}, "user": {}}))
    assert api_publish.call_count == 3


async def test_publish(mocker):
    run_in_threadpool = mocker.patch("fmn.api.messaging.run_in_threadpool", new=mock.MagicMock())
    run_in_threadpool.return_value = awaitable_sentinel = object()
    create_task = mocker.patch("asyncio.create_task")

    message = RuleCreateV1({"rule": {}, "user": {}})

    await messaging.publish(message)

    run_in_threadpool.assert_called_with(messaging._publish, message=message)
    create_task.assert_called_with(awaitable_sentinel)
