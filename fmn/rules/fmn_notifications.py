def fmn_confirmation_update(config, message):
    """ Notifications: The status of confirmation changed

    Adding this rule to your filters will let through messages
    from `Notifications <https://apps.fedoraproject.org/notifications>`_
    whenever the status of confirmation changes.
    """
    return message['topic'].endswith('fmn.confirmation.update')


def fmn_filter_update(config, message):
    """ Notifications: Someone updated one of their notification rules

    Adding this rule to your filters will let through messages
    from `Notifications <https://apps.fedoraproject.org/notifications>`_
    whenever someone updates one of their notification rules.
    """
    return message['topic'].endswith('fmn.filter.update')


def fmn_preference_update(config, message):
    """ Notifications: Someone updated their delivery details

    Adding this rule to your filters will let through messages
    from `Notifications <https://apps.fedoraproject.org/notifications>`_
    whenever someone **updates their delivery details**.
    """
    return message['topic'].endswith('fmn.preference.update')


