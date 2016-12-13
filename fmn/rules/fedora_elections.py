from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('fedora_elections.candidate.delete')])
def fedora_elections_candidate_delete(config, message):
    """ Candidates are deleted from an election.

    Adding this rule will let through elections from `Fedora
    Elections <https://apps.fedoraproject.org/voting/>`_ whenever
    a candidate is deleted in an election.
    """
    return message['topic'].endswith('fedora_elections.candidate.delete')


@hint(topics=[_('fedora_elections.candidate.edit')])
def fedora_elections_candidate_edit(config, message):
    """ Candidates are updated in an election.

    Adding this rule will let through elections from `Fedora
    Elections <https://apps.fedoraproject.org/voting/>`_ whenever a
    candidate is edited in an election.
    """
    return message['topic'].endswith('fedora_elections.candidate.edit')


@hint(topics=[_('fedora_elections.candidate.new')])
def fedora_elections_candidate_new(config, message):
    """ New candidates are added to an election.

    Adding this rule will let through elections from `Fedora
    Elections <https://apps.fedoraproject.org/voting/>`_ whenever a
    candidate is added in an election.
    """
    return message['topic'].endswith('fedora_elections.candidate.new')


@hint(topics=[_('fedora_elections.election.edit')])
def fedora_elections_election_edit(config, message):
    """ Elections are updated

    Adding this rule will let through elections from `Fedora
    Elections <https://apps.fedoraproject.org/voting/>`_ whenever someone
    edits the metadata of an election.
    """
    return message['topic'].endswith('fedora_elections.election.edit')


@hint(topics=[_('fedora_elections.election.new')])
def fedora_elections_election_new(config, message):
    """ New elections

    Adding this rule will let through elections from `Fedora
    Elections <https://apps.fedoraproject.org/voting/>`_ whenever someone
    creates a new election.
    """
    return message['topic'].endswith('fedora_elections.election.new')
