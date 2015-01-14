from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['copr'])
def copr_catchall(config, message):
    """ All Copr events

    Adding this rule will indiscriminately match notifications of all types
    from `copr <https://copr.fedoraproject.org>`_, i.e. new
    and finished builds, newly spun up workers and chroots, etc..
    """
    return message['topic'].split('.')[3] == 'copr'


@hint(topics=[_('copr.build.start')])
def copr_build_start(config, message):
    """ Copr builds starting

    `Copr <https://copr.fedoraproject.org/>`_ publishes messages
    when a new build starts.  Adding this rule will get you those messages.
    """
    return message['topic'].endswith('copr.build.start')


@hint(topics=[_('copr.build.end')])
def copr_build_end(config, message):
    """ Copr builds ending

    `Copr <https://copr.fedoraproject.org/>`_ publishes messages
    when a new build ends.  Adding this rule will get you those messages.
    """
    return message['topic'].endswith('copr.build.end')


@hint(topics=[_('copr.build.end')], invertible=False)
def copr_build_failed(config, message):
    """ Copr builds failing

    `Copr <https://copr.fedoraproject.org/>`_ publishes messages
    when a new build fails.  Adding this rule will get you those messages.
    """
    if not copr_build_end(config, message):
        return False

    return message['msg']['status'] == 0


@hint(topics=[_('copr.build.end')], invertible=False)
def copr_build_success(config, message):
    """ Copr builds succeeding

    `Copr <https://copr.fedoraproject.org/>`_ publishes messages
    when a new build successfully ends.  Adding this rule will get you those messages.
    """
    if not copr_build_end(config, message):
        return False

    return message['msg']['status'] == 1


@hint(topics=[_('copr.build.end')], invertible=False)
def copr_build_skipped(config, message):
    """ Copr builds skipped

    `Copr <https://copr.fedoraproject.org/>`_ publishes messages
    when a new build is skipped.  Adding this rule will get you those messages.
    """
    if not copr_build_end(config, message):
        return False

    return message['msg']['status'] == 5


@hint(topics=[_('copr.chroot.start')])
def copr_chroot_start(config, message):
    """ New Copr chroots

    `Copr <https://copr.fedoraproject.org/>`_ publishes messages
    when a new chroot starts.  Adding this rule will get you those messages.
    """
    return message['topic'].endswith('copr.chroot.start')


@hint(topics=[_('copr.worker.create')])
def copr_worker_create(config, message):
    """ New Copr workers are spun up

    `Copr <https://copr.fedoraproject.org/>`_ publishes messages
    when a new worker is created.  Adding this rule will get you those
    messages.
    """
    return message['topic'].endswith('copr.worker.create')
