
def fedocal_calendar_clear(config, message):
    """ Calendar:  An admin has cleared all meetings from a calendar.

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/calendar>`_ whenever someone clears all
    meetings from a calendar there.
    """
    return message['topic'].endswith('fedocal.calendar.clear')


def fedocal_calendar_create(config, message):
    """ Calendar:  An admin has created a new calendar.

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/calendar>`_ whenever someone creates a
    new calendar.
    """
    return message['topic'].endswith('fedocal.calendar.new')


def fedocal_calendar_delete(config, message):
    """ Calendar:  An admin has deleted a calendar.

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/calendar>`_ whenever someone deletes a
    calendar.
    """
    return message['topic'].endswith('fedocal.calendar.delete')


def fedocal_calendar_update(config, message):
    """ Calendar:  An admin has updated a calendar.

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/calendar>`_ whenever someone updates a
    calendar.
    """
    return message['topic'].endswith('fedocal.calendar.update')


def fedocal_meeting_create(config, message):
    """ Meeting:  Someone created a new meeting.

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/meeting>`_ whenever someone creates a
    new meeting.
    """
    return message['topic'].endswith('fedocal.meeting.new')


def fedocal_meeting_update(config, message):
    """ Meeting:  Someone updated a meeting.

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/meeting>`_ whenever someone updates an
    existing meeting.
    """
    return message['topic'].endswith('fedocal.meeting.update')


def fedocal_meeting_delete(config, message):
    """ Meeting:  Someone deleted a meeting.

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/meeting>`_ whenever someone deletes an
    existing meeting.
    """
    return message['topic'].endswith('fedocal.meeting.delete')


def fedocal_meeting_reminder(config, message):
    """ Meeting:  Automatic upcoming meeting reminders.

    Adding this rule will let through scheduled notifications from `Fedocal
    <https://apps.fedoraproject.org/meeting>`_ whenever a meeting is
    approaching.
    """
    return message['topic'].endswith('fedocal.meeting.reminder')
