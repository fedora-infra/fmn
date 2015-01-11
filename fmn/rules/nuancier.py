from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('nuancier.candidate.approved')])
def nuancier_candidate_approved(config, message):
    """ Approved wallpaper candidates

    Adding this rule to your filters will let through messages
    from `Nuancier <https://apps.fedoraproject.org/nuancier>`_
    when an admin **approves** a candidate submission.
    """
    return message['topic'].endswith('nuancier.candidate.approved')


@hint(topics=[_('nuancier.candidate.denied')])
def nuancier_candidate_denied(config, message):
    """ Denied wallpaper candidates

    Adding this rule to your filters will let through messages
    from `Nuancier <https://apps.fedoraproject.org/nuancier>`_
    when an admin **denies** a candidate submission.
    """
    return message['topic'].endswith('nuancier.candidate.denied')


@hint(topics=[_('nuancier.candidate.new')])
def nuancier_candidate_new(config, message):
    """ New wallpaper candidates

    Adding this rule to your filters will let through messages
    from `Nuancier <https://apps.fedoraproject.org/nuancier>`_
    when *a contributor submits a new candidate* for existing election.
    """
    return message['topic'].endswith('nuancier.candidate.new')


@hint(topics=[_('nuancier.election.new')])
def nuancier_election_new(config, message):
    """ New wallpaper elections are set up

    Adding this rule to your filters will let through messages
    from `Nuancier <https://apps.fedoraproject.org/nuancier>`_
    when *an admin creates a new election*.
    """
    return message['topic'].endswith('nuancier.election.new')


@hint(topics=[_('nuancier.election.update')])
def nuancier_election_update(config, message):
    """ Existing wallpaper elections are modified

    Adding this rule to your filters will let through messages
    from `Nuancier <https://apps.fedoraproject.org/nuancier>`_
    when *an admin updates the details of a election*.
    """
    return message['topic'].endswith('nuancier.election.update')
