def fedora_elections_candidate_delete(config, message):
    """ Elections: A candidate was deleted from an election.

    Adding this rule will let through elections from `Fedora
    Elections <https://apps.fedoraproject.org/voting/>`_ whenever
    a candidate is deleted in an election.
    """
    return message['topic'].endswith('fedora_elections.candidate.delete')


def fedora_elections_candidate_edit(config, message):
    """ Elections: A candidate was edited in an election.

    Adding this rule will let through elections from `Fedora
    Elections <https://apps.fedoraproject.org/voting/>`_ whenever a
    candidate is edited in an election.
    """
    return message['topic'].endswith('fedora_elections.candidate.edit')


def fedora_elections_candidate_new(config, message):
    """ Elections: A candidate is added to an election.

    Adding this rule will let through elections from `Fedora
    Elections <https://apps.fedoraproject.org/voting/>`_ whenever a
    candidate is added in an election.
    """
    return message['topic'].endswith('fedora_elections.candidate.new')


def fedora_elections_election_edit(config, message):
    """ Elections: Someone edited an election.

    Adding this rule will let through elections from `Fedora
    Elections <https://apps.fedoraproject.org/voting/>`_ whenever someone
    edits an election.
    """
    return message['topic'].endswith('fedora_elections.election.edit')


def fedora_elections_election_new(config, message):
    """ Elections: Someone created a new election.

    Adding this rule will let through elections from `Fedora
    Elections <https://apps.fedoraproject.org/voting/>`_ whenever someone
    creates a new election.
    """
    return message['topic'].endswith('fedora_elections.election.new')
