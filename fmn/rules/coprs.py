def copr_build_start(config, message):
    """ Copr:  Build started

    `Copr <https://fedorahosted.org/copr/>`_ publishes messages
    when a new build starts.  Adding this rule will get you those messages.
    """
    return message['topic'].endswith('copr.build.start')


def copr_build_end(config, message):
    """ Copr:  Build ended

    `Copr <https://fedorahosted.org/copr/>`_ publishes messages
    when a new build ends.  Adding this rule will get you those messages.
    """
    return message['topic'].endswith('copr.build.end')


def copr_build_failed(config, message):
    """ Copr:  Build failed

    `Copr <https://fedorahosted.org/copr/>`_ publishes messages
    when a new build fails.  Adding this rule will get you those messages.
    """
    if not copr_build_end(config, message):
        return False

    return message['msg']['status'] == 0


def copr_build_success(config, message):
    """ Copr:  Build successfully ended

    `Copr <https://fedorahosted.org/copr/>`_ publishes messages
    when a new build successfully ends.  Adding this rule will get you those messages.
    """
    if not copr_build_end(config, message):
        return False

    return message['msg']['status'] == 1


def copr_build_skipped(config, message):
    """ Copr:  Build skipped

    `Copr <https://fedorahosted.org/copr/>`_ publishes messages
    when a new build is skipped.  Adding this rule will get you those messages.
    """
    if not copr_build_end(config, message):
        return False

    return message['msg']['status'] == 5


def copr_chroot_start(config, message):
    """ Copr:  chroot started

    `Copr <https://fedorahosted.org/copr/>`_ publishes messages
    when a new chroot starts.  Adding this rule will get you those messages.
    """
    return message['topic'].endswith('copr.chroot.start')


def copr_worker_create(config, message):
    """ Copr:  worker created

    `Copr <https://fedorahosted.org/copr/>`_ publishes messages
    when a new worker is created.  Adding this rule will get you those
    messages.
    """
    return message['topic'].startswith('copr.worker.create')
