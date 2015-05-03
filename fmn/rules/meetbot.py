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


@hint(topics=[_('meetbot.meeting.agreed')])
def meetbot_meeting_agreed(config, message):
    """ Points agreed upon in IRC meetings

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  This rule catches the messages that get published when
    people use the ``#agree`` directive in a meeting.
    """
    return message['topic'].endswith('meetbot.meeting.agreed')


@hint(topics=[_('meetbot.meeting.accepted')])
def meetbot_meeting_accepted(config, message):
    """ Points accepted in IRC meetings

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  This rule catches the messages that get published when
    people use the ``#accept`` directive in a meeting.
    """
    return message['topic'].endswith('meetbot.meeting.accepted')


@hint(topics=[_('meetbot.meeting.rejected')])
def meetbot_meeting_rejected(config, message):
    """ Points rejected in IRC meetings

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  This rule catches the messages that get published when
    people use the ``#reject`` directive in a meeting.
    """
    return message['topic'].endswith('meetbot.meeting.rejected')


@hint(topics=[_('meetbot.meeting.action')])
def meetbot_meeting_action(config, message):
    """ Action items from IRC meetings

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  This rule catches the messages that get published when
    people use the ``#action`` directive in a meeting.
    """
    return message['topic'].endswith('meetbot.meeting.action')


@hint(topics=[_('meetbot.meeting.info')])
def meetbot_meeting_info(config, message):
    """ Informational items from IRC meetings

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  This rule catches the messages that get published when
    people use the ``#info`` directive in a meeting.
    """
    return message['topic'].endswith('meetbot.meeting.info')


@hint(topics=[_('meetbot.meeting.idea')])
def meetbot_meeting_idea(config, message):
    """ Ideas from IRC meetings

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  This rule catches the messages that get published when
    people use the ``#idea`` directive in a meeting.
    """
    return message['topic'].endswith('meetbot.meeting.idea')


@hint(topics=[_('meetbot.meeting.help')])
def meetbot_meeting_help(config, message):
    """ Calls for help from IRC meetings

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  This rule catches the messages that get published when
    people use the ``#help`` directive in a meeting.
    """
    return message['topic'].endswith('meetbot.meeting.help')


@hint(topics=[_('meetbot.meeting.link')])
def meetbot_meeting_link(config, message):
    """ Links from IRC meetings

    Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
    messages too!  This rule catches the messages that get published when
    people use the ``#link`` directive in a meeting.
    """
    return message['topic'].endswith('meetbot.meeting.link')
