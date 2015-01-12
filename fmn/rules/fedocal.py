from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['fedocal'])
def fedocal_catchall(config, message):
    """ All Fedora Calendar events

    Adding this rule will indiscriminately match notifications of all types
    from the `Fedocal Calendaring System
    <https://apps.fedoraproject.org/calendar>`_, i.e. messages about new
    calendars, new meetings, and more.
    """
    return message['topic'].split('.')[3] == 'fedocal'


@hint(topics=[_('fedocal.calendar.clear')])
def fedocal_calendar_clear(config, message):
    """ When an admin has cleared all meetings from a calendar.

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/calendar>`_ whenever someone clears all
    meetings from a calendar there.
    """
    return message['topic'].endswith('fedocal.calendar.clear')


@hint(topics=[_('fedocal.calendar.new')])
def fedocal_calendar_create(config, message):
    """ New fedocal calendars

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/calendar>`_ whenever someone creates a
    new calendar.
    """
    return message['topic'].endswith('fedocal.calendar.new')


@hint(topics=[_('fedocal.calendar.delete')])
def fedocal_calendar_delete(config, message):
    """ Old fedocal calendars are deleted

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/calendar>`_ whenever someone deletes a
    calendar.
    """
    return message['topic'].endswith('fedocal.calendar.delete')


@hint(topics=[_('fedocal.calendar.update')])
def fedocal_calendar_update(config, message):
    """ Fedocal calendars get their metadata updated

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/calendar>`_ whenever someone updates a
    calendar.
    """
    return message['topic'].endswith('fedocal.calendar.update')


@hint(topics=[_('fedocal.meeting.new')])
def fedocal_meeting_create(config, message):
    """ New meetings scheduled in fedocal

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/meeting>`_ whenever someone creates a
    new meeting.
    """
    return message['topic'].endswith('fedocal.meeting.new')


@hint(topics=[_('fedocal.meeting.update')])
def fedocal_meeting_update(config, message):
    """ Updated fedocal meetings

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/meeting>`_ whenever someone updates an
    existing meeting.
    """
    return message['topic'].endswith('fedocal.meeting.update')


@hint(topics=[_('fedocal.meeting.delete')])
def fedocal_meeting_delete(config, message):
    """ Fedocal meetings are deleted

    Adding this rule will let through notifications from `Fedocal
    <https://apps.fedoraproject.org/meeting>`_ whenever someone deletes an
    existing meeting.
    """
    return message['topic'].endswith('fedocal.meeting.delete')


@hint(topics=[_('fedocal.meeting.reminder')])
def fedocal_meeting_reminder(config, message):
    """ Fedocal meeting reminders

    Adding this rule will let through scheduled notifications from `Fedocal
    <https://apps.fedoraproject.org/meeting>`_ whenever a meeting is
    approaching.
    """
    return message['topic'].endswith('fedocal.meeting.reminder')
