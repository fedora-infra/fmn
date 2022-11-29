from fedora_messaging import exceptions as fm_exceptions

from fmn.api import messaging
from fmn.messages.rule import RuleCreateV1


def test_publish(mocker):
    api_publish = mocker.patch("fedora_messaging.api.publish")
    messaging.publish(RuleCreateV1({"rule": {}, "user": {}}))
    api_publish.assert_called_once()


def test_publish_with_errors(mocker):
    api_publish = mocker.patch("fedora_messaging.api.publish")
    api_publish.side_effect = fm_exceptions.ConnectionException()
    messaging.publish(RuleCreateV1({"rule": {}, "user": {}}))
    assert api_publish.call_count == 3
