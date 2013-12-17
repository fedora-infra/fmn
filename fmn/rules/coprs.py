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
