def meetbot_meeting_complete(config, message):
    """ Meetbot: Meeting completed

Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
messages too!  Messages on this topic get published when an IRC meeting
ends.  Meetings may or may not have a title (which can be tricky).
Here's an example message where the title is specified:

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('meetbot.meeting.complete')


def meetbot_meeting_start(config, message):
    """ Meetbot: Meeting started

Trusty old `zodbot <https://meetbot.fedoraproject.org/>`_ publishes
messages too!  Messages on this topic get published (somewhat obviously)
when a new IRC meeting is started.  The user starting the meeting may
specify a meeting title, but doesn't have to.  Here's an example
message with a specified meeting title:

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('meetbot.meeting.start')



def meetbot_meeting_topic_update(config, message):
    """ Meetbot: Topic of a meeting changed

As IRC meetings chug along, the chairperson may change the meeting;
zodbot publishes message for that!  An example **with** a title specified:

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('meetbot.meeting.topic.update')
