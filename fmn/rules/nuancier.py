def nuancier_candidate_approved(config, message):
    """ Nuancier: An admin approved a candidate submission

    Adding this rule to your filters will let through messages
    from `Nuancier <https://apps.fedoraproject.org/nuancier>`_
    when an admin **approves** a candidate submission.
    """
    return message['topic'].endswith('nuancier.candidate.approved')


def nuancier_candidate_denied(config, message):
    """ Nuancier: An admin denied a candidate submission

    Adding this rule to your filters will let through messages
    from `Nuancier <https://apps.fedoraproject.org/nuancier>`_
    when an admin **denies** a candidate submission.
    """
    return message['topic'].endswith('nuancier.candidate.denied')


def nuancier_candidate_new(config, message):
    """ Nuancier: A contributor submitted a new candidate

    Adding this rule to your filters will let through messages
    from `Nuancier <https://apps.fedoraproject.org/nuancier>`_
    when *a contributor submits a new candidate* for existing election.
    """
    return message['topic'].endswith('nuancier.candidate.new')


def nuancier_election_new(config, message):
    """ Nuancier: An admin created a new election

    Adding this rule to your filters will let through messages
    from `Nuancier <https://apps.fedoraproject.org/nuancier>`_
    when *an admin creates a new election*. 
    """
    return message['topic'].endswith('nuancier.election.new')


def nuancier_election_update(config, message):
    """ Nuancier: An admin updated details of a election

    Adding this rule to your filters will let through messages
    from `Nuancier <https://apps.fedoraproject.org/nuancier>`_
    when *an admin updates the details of a election*. 
    """
    return message['topic'].endswith('nuancier.election.update')


