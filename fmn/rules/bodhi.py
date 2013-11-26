

def bodhi_buildroot_override_tag(config, message):
    """ Bodhi: A user requested a buildroot override

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.override.tag')


def bodhi_buildroot_override_untag(config, message):
    """ Bodhi: A user removed a buildroot override

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.override.untag')


def bodhi_mashtask_complete(config, message):
    """ Bodhi: Masher finished its work

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.mashtask.complete')


def bodhi_mashtask_mashing(config, message):
    """ Bodhi: Masher started on a particular repository

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.mashtask.mashing')


def bodhi_mashtask_start(config, message):
    """ Bodhi: Masher started working

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.mashtask.start')


def bodhi_mashtask_sync_done(config, message):
    """ Bodhi: Masher finished syncing

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.mashtask.sync.done')


def bodhi_mashtask_sync_wait(config, message):
    """ Bodhi: Masher starts waiting to sync

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.mashtask.sync.wait')


def bodhi_update_comment(config, message):
    """ Bodhi: a user added a comment to a bodhi update

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.update.comment')


def bodhi_update_complete_testing(config, message):
    """ Bodhi: update has been pushed to the testing repository

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.update.complete.testing')


def bodhi_update_request_obsolete(config, message):
    """ Bodhi: a user requested an update be obsoleted

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.update.request.obsolete')


def bodhi_update_request_revoke(config, message):
    """ Bodhi: a user revoked a prior request on an update

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.update.request.revoke')


def bodhi_update_request_stable(config, message):
    """ Bodhi: a user requested an update be marked as stable

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.update.request.stable')


def bodhi_update_request_testing(config, message):
    """ Bodhi: a user requested an update be pushed to testing

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.update.request.stable')


def bodhi_update_request_unpush(config, message):
    """ Bodhi: a user requested an update be unpushed

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('bodhi.update.request.unpush')
