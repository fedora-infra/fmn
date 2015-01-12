from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('fas.group.create')])
def fas_group_create(config, message):
    """ New FAS groups

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **new group has been created**.
    """
    return message['topic'].endswith('fas.group.create')


@hint(topics=[_('fas.group.member.apply')])
def fas_group_member_apply(config, message):
    """ Members apply to FAS groups

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **user has requested to join a group**.
    """
    return message['topic'].endswith('fas.group.member.apply')


@hint(topics=[_('fas.group.member.remove')])
def fas_group_member_remove(config, message):
    """ Members are removed from FAS groups

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **user was removed from a group**.
    """
    return message['topic'].endswith('fas.group.member.remove')


@hint(topics=[_('fas.group.member.sponsor')])
def fas_group_member_sponsor(config, message):
    """ Members are sponsored in to FAS groups

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **user has been sponsored into a group**.
    """
    return message['topic'].endswith('fas.group.member.sponsor')


@hint(topics=[_('fas.group.update')])
def fas_group_update(config, message):
    """ FAS groups information changes

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **group's details were updated**.
    """
    return message['topic'].endswith('fas.group.update')


@hint(topics=[_('fas.role.update')])
def fas_role_update(config, message):
    """ Role changes for users in a FAS group

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **user's role in a group was updated**.
    """
    return message['topic'].endswith('fas.role.update')


@hint(topics=[_('fas.user.create')])
def fas_user_create(config, message):
    """ New FAS accounts

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **new user was created**.
    """
    return message['topic'].endswith('fas.user.create')


@hint(topics=[_('fas.user.update')])
def fas_user_update(config, message):
    """ Updates to FAS accounts

    Adding this rule to a filter will allow through `Fedora Account System
    <https://admin.fedoraproject.org/accounts>`_ notifications indicating that
    a **user updated their account information**.
    """
    return message['topic'].endswith('fas.user.update')
