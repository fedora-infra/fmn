def fas_group_create(config, message):
    """ FAS: New group created

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **new group has been created**.
    """
    return message['topic'].endswith('fas.group.create')


def fas_group_member_apply(config, message):
    """ FAS: A member requested to join a group

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **user has requested to join a group**.
    """
    return message['topic'].endswith('fas.group.member.apply')


def fas_group_member_remove(config, message):
    """ FAS: A user was removed from a group

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **user was removed from a group**.
    """
    return message['topic'].endswith('fas.group.member.remove')


def fas_group_member_sponsor(config, message):
    """ FAS: A user has been sponsored by an authorized user into a group

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **user has been sponsored into a group**.
    """
    return message['topic'].endswith('fas.group.member.sponsor')


def fas_group_update(config, message):
    """ FAS: A group's properties have been modified

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **group's details were updated**.
    """
    return message['topic'].endswith('fas.group.update')


def fas_role_update(config, message):
    """ FAS: A user's role in a particular group has been updated

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **user's role in a group was updated**.
    """
    return message['topic'].endswith('fas.role.update')


def fas_user_create(config, message):
    """ FAS: A new user account has been created

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **new user was created**.
    """
    return message['topic'].endswith('fas.user.create')


def fas_user_update(config, message):
    """ FAS: A user updated his/her account

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **user updated their account information**.
    """
    return message['topic'].endswith('fas.user.update')
