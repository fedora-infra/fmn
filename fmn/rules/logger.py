from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('logger.log')])
def logger_log(config, message):
    """ Admin logging and debug statements

    Include this rule to receive notifications of messages being sent by an
    admin who uses `fedmsg-logger` on a host, and doesn't explicitly provide
    a topic for the message to get sent as. This is usually used for testing.
    """
    return message['topic'].endswith('logger.log')
