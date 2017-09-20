"""
The FMN consumer package contains all the service that process the incoming
`fedmsg`_ messages. The messages are processed in three steps:

1. The `fedmsg consumer`_ defined in :mod:`fmn.consumer.consumer` subscribes
   to every fedmsg topic (``*``). It uses Celery to dispatch tasks to a
   message queue called ``worker``. This message broker provides message
   durability for FMN as it processes the messages.

2. One or more Celery worker processes are started and consume
   messages from the ``worker`` message queue. These worker processes take
   each message and determine who should receive notifications based on their
   message filters. It then records this information in the message and
   publishes the message to the ``backend`` queue.

3. A single :mod:`fmn.consumer.backend` process is run and is responsible for
   sending the messages to users via IRC, email, etc. It consumes the messages
   from the ``backend`` queue and dispatches them. It defines a backend interface
   and new backends can be added to allow for new message mediums.
"""
from .. import fmn_fasshim  # noqa
from .consumer import FMNConsumer  # noqa
from .producer import ConfirmationProducer  # noqa
from .producer import DigestProducer  # noqa
