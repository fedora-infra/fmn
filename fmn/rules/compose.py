from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['compose'])
def compose_catchall(config, message):
    """ All compose events

    Adding this rule will indiscriminately match notifications of all types
    from the `compose process <https://apps.fedoraproject.org/releng-dash>`_.
    """
    return message['topic'].split('.')[3] == 'compose'


@hint(topics=[_('compose.branched.complete')])
def compose_branched_complete(config, message):
    """ Compose completed for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **entire** `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    the 'branched' Fedora pre-release.
    """
    return message['topic'].endswith('compose.branched.complete')


@hint(topics=[_('compose.branched.mash.complete')])
def compose_branched_mash_complete(config, message):
    """ Mash completed for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **mash** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of the 'branched' Fedora
    pre-release.
    """
    return message['topic'].endswith('compose.branched.mash.complete')


@hint(topics=[_('compose.branched.mash.start')])
def compose_branched_mash_start(config, message):
    """ Mash started for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the **mash** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of the 'branched' Fedora
    pre-release.
    """
    return message['topic'].endswith('compose.branched.mash.start')


@hint(topics=[_('compose.branched.pungify.complete')])
def compose_branched_pungify_complete(config, message):
    """ Pungi completed for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **pungi** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of the 'branched' Fedora
    pre-release.
    """
    return message['topic'].endswith('compose.branched.pungify.complete')


@hint(topics=[_('compose.branched.pungify.start')])
def compose_branched_pungify_start(config, message):
    """ Pungi started for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the **pungi** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of the 'branched' Fedora
    pre-release.
    """
    return message['topic'].endswith('compose.branched.pungify.start')


@hint(topics=[_('compose.branched.rsync.complete')])
def compose_branched_rsync_complete(config, message):
    """ rsync completed for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ finishes
    **rsyncing** a `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    the 'branched' Fedora pre-release.
    """
    return message['topic'].endswith('compose.branched.rsync.complete')


@hint(topics=[_('compose.branched.rsync.start')])
def compose_branched_rsync_start(config, message):
    """ rsync started for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    **rsyncing** a `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    the 'branched' Fedora pre-release.
    """
    return message['topic'].endswith('compose.branched.rsync.start')


@hint(topics=[_('compose.branched.start')])
def compose_branched_start(config, message):
    """ Compose started for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the `compose <https://apps.fedoraproject.org/releng-dash/>`_ process for
    the 'branched' Fedora pre-release.
    """
    return message['topic'].endswith('compose.branched.start')


@hint(topics=[_('compose.epelbeta.complete')])
def compose_epelbeta_complete(config, message):
    """ Compose completed for epelbeta

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **entire** `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    EPEL beta.
    """
    return message['topic'].endswith('compose.epelbeta.complete')


@hint(topics=[_('compose.rawhide.complete')])
def compose_rawhide_complete(config, message):
    """ Compose completed for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **entire** `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    rawhide.
    """
    return message['topic'].endswith('compose.rawhide.complete')


@hint(topics=[_('compose.rawhide.mash.complete')])
def compose_rawhide_mash_complete(config, message):
    """ Mash completed for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **mash** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of rawhide.
    """
    return message['topic'].endswith('compose.rawhide.mash.complete')


@hint(topics=[_('compose.rawhide.mash.start')])
def compose_rawhide_mash_start(config, message):
    """ Mash started for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the **mash** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of rawhide.
    """
    return message['topic'].endswith('compose.rawhide.mash.start')


@hint(topics=[_('compose.rawhide.pungify.complete')])
def compose_rawhide_pungify_complete(config, message):
    """ Pungi completed for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **pungi** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of rawhide.
    """
    return message['topic'].endswith('compose.rawhide.pungify.complete')


@hint(topics=[_('compose.rawhide.pungify.start')])
def compose_rawhide_pungify_start(config, message):
    """ Pungi started for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the **pungi** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of rawhide.
    """
    return message['topic'].endswith('compose.rawhide.pungify.start')


@hint(topics=[_('compose.rawhide.rsync.complete')])
def compose_rawhide_rsync_complete(config, message):
    """ rsync completed for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ finishes
    **rsyncing** a `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    rawhide.
    """
    return message['topic'].endswith('compose.rawhide.rsync.complete')


@hint(topics=[_('compose.rawhide.rsync.start')])
def compose_rawhide_rsync_start(config, message):
    """ rsync started for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    **rsyncing** a `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    rawhide.
    """
    return message['topic'].endswith('compose.rawhide.rsync.start')


@hint(topics=[_('compose.rawhide.start')])
def compose_rawhide_start(config, message):
    """ Compose started for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the `compose <https://apps.fedoraproject.org/releng-dash/>`_ process for
    rawhide.
    """
    return message['topic'].endswith('compose.rawhide.start')
