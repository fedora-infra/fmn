def bodhi_buildroot_override_tag(config, message):
    """ Bodhi: A user requested a buildroot override

    Adding this rule will allow through notifications whenever a user
    **requests a buildroot override** via the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_.
    """
    return message['topic'].endswith('bodhi.override.tag')


def bodhi_buildroot_override_untag(config, message):
    """ Bodhi: A user removed a buildroot override

    Adding this rule will allow through notifications whenever a user
    **delets a request for a buildroot override** via the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_.
    """
    return message['topic'].endswith('bodhi.override.untag')


def bodhi_update_comment(config, message):
    """ Bodhi: a user added a comment to a bodhi update

    As part of the QA process, users may comment on updates in
    the `Bodhi Updates System <https://admin.fedoraproject.org/updates>`_.
    This rule will let through messages indicating that they have done so.
    """
    return message['topic'].endswith('bodhi.update.comment')

def bodhi_update_request_obsolete(config, message):
    """ Bodhi: a user requested an update be obsoleted

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ indicating that a user has
    *requested* that an updated be **obsoleted**.
    """
    return message['topic'].endswith('bodhi.update.request.obsolete')


def bodhi_update_request_revoke(config, message):
    """ Bodhi: a user revoked a prior request on an update

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ indicating that a user has
    *requested* that an updated be **revoked**.
    """
    return message['topic'].endswith('bodhi.update.request.revoke')


def bodhi_update_request_stable(config, message):
    """ Bodhi: a user requested an update be marked as stable

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ indicating that a user has
    *requested* that an updated be **pushed to stable**.
    """
    return message['topic'].endswith('bodhi.update.request.stable')


def bodhi_update_request_testing(config, message):
    """ Bodhi: a user requested an update be pushed to testing

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ indicating that a user has
    *requested* that an updated be **pushed to testing**.
    """
    return message['topic'].endswith('bodhi.update.request.testing')


def bodhi_update_request_unpush(config, message):
    """ Bodhi: a user requested an update be unpushed

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ indicating that a user has
    *requested* that an updated be **unpushed**.
    """
    return message['topic'].endswith('bodhi.update.request.unpush')
