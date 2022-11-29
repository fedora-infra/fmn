import logging
import sys
import traceback

import backoff
from fedora_messaging import api
from fedora_messaging import exceptions as fm_exceptions

log = logging.getLogger(__name__)


def backoff_hdlr(details):
    log.warning(f"Publishing message failed. Retrying. {traceback.format_tb(sys.exc_info()[2])}")


@backoff.on_exception(
    backoff.expo,
    (fm_exceptions.ConnectionException, fm_exceptions.PublishException),
    max_tries=3,
    on_backoff=backoff_hdlr,
)
def _publish(message):
    api.publish(message)


def publish(message):
    try:
        _publish(message)
    except (fm_exceptions.BaseException):
        log.error(f"Publishing message failed. Giving up. {traceback.format_tb(sys.exc_info()[2])}")
        return
