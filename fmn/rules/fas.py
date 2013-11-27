def fas_group_create(config, message):
    """ Fas: New group created.

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fas.group.create')


def fas_group_member_apply(config, message):
    """ Fas: A member requested to join a group.

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fas.group.member.apply')


def fas_group_member_remove(config, message):
    """ Fas: A user was removed from a group.

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fas.group.member.remove')


def fas_group_member_sponsor(config, message):
    """ Fas: A user has been sponsored by an authorized user into a group.

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fas.group.member.sponsor')


def fas_group_update(config, message):
    """ Fas: A group's properties have been modified.

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fas.group.update')


def fas_role_update(config, message):
    """ A user's role in a particular group has been updated.

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fas.role.update')


def fas_user_create(config, message):
    """ Fas: A new user account has been created.

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fas.user.create')


def fas_user_update(config, message):
    """ Fas: A user updated his/her account.

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fas.user.update')
