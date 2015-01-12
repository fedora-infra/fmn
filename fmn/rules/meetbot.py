from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['meetbot'])
def meetbot_catchall(config, message):
    """ All IRC meeting events

    Adding this rule will indiscriminately match notifications of all types
    from trusty old `zodbot <https://meetbot.fedoraproject.org/>`_.  It
    publishes messages about IRC meetings stopping, starting, changing,.. etc,
    as they occur.
    """
    return message['topic'].split('.')[3] == 'meetbot'


@hint(topics=[_('meetbot.meeting.complete')])
def meetbot_meeting_complete(config, message):
    """ IRC meetings ending

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  Adding this rule will notify you when an IRC meeting
    ends.
    """
    return message['topic'].endswith('meetbot.meeting.complete')


@hint(topics=[_('meetbot.meeting.start')])
def meetbot_meeting_start(config, message):
    """ IRC meetings starting

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  Adding this rule will notify you (perhaps obviously)
    when a new IRC meeting is started.
    """
    return message['topic'].endswith('meetbot.meeting.start')


@hint(topics=[_('meetbot.meeting.topic.update')])
def meetbot_meeting_topic_update(config, message):
    """ IRC meeting topic changes

    As IRC meetings chug along, the chairperson may change the meeting;
    zodbot publishes message for that!  Guess what?  Adding this rule will let
    you get notifications about that.
    """
    return message['topic'].endswith('meetbot.meeting.topic.update')
