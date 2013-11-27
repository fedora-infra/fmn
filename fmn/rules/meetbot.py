def meetbot_meeting_complete(config, message):
    """ Meetbot: Meeting completed

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  Adding this rule will notify you when an IRC meeting
    ends.
    """
    return message['topic'].endswith('meetbot.meeting.complete')


def meetbot_meeting_start(config, message):
    """ Meetbot: Meeting started

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  Adding this rule will notify you (perhaps obviously)
    when a new IRC meeting is started.
    """
    return message['topic'].endswith('meetbot.meeting.start')


def meetbot_meeting_topic_update(config, message):
    """ Meetbot: Topic of a meeting changed

    As IRC meetings chug along, the chairperson may change the meeting;
    zodbot publishes message for that!  Guess what?  Adding this rule will let
    you get notifications about that.
    """
    return message['topic'].endswith('meetbot.meeting.topic.update')
