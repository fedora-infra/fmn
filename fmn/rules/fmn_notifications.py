from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['fmn'])
def fmn_catchall(config, message):
    """ All FMN meta-notification stuff

    Adding this rule will indiscriminately match notifications of all types
    from `this service <https://apps.fedoraproject.org/notifications>`_.  Those
    kinds of messages include account, profile, and notification-preference
    changes.
    """
    return message['topic'].split('.')[3] == 'fmn'


@hint(topics=[_('fmn.confirmation.update')])
def fmn_confirmation_update(config, message):
    """ Confirmation status changes (FMN)

    Adding this rule to your filters will let through messages
    from `Notifications <https://apps.fedoraproject.org/notifications>`_
    whenever the status of confirmation changes.
    """
    return message['topic'].endswith('fmn.confirmation.update')


@hint(topics=[_('fmn.filter.update')])
def fmn_filter_update(config, message):
    """ Notification filter changes (FMN)

    Adding this rule to your filters will let through messages
    from `Notifications <https://apps.fedoraproject.org/notifications>`_
    whenever someone updates one of their notification rules.
    """
    return message['topic'].endswith('fmn.filter.update')


@hint(topics=[_('fmn.preference.update')])
def fmn_preference_update(config, message):
    """ Notification profile changes (FMN)

    Adding this rule to your filters will let through messages
    from `Notifications <https://apps.fedoraproject.org/notifications>`_
    whenever someone **updates their delivery details**.
    """
    return message['topic'].endswith('fmn.preference.update')
