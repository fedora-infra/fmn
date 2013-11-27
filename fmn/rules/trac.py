def trac_git_receive(config, message):
    """ Fedora Hosted: Commits pushed to a git repository

    Adding this rule will get you notifications when a user **pushes commits**
    to a `fedorahosted <https://fedorahosted.org>`_ git repository.
    """
    return message['topic'].endswith('trac.git.receive')


def trac_ticket_delete(config, message):
    """ Fedora Hosted: Deleted a ticket on a trac instance

    Adding this rule will get you notifications when a user **deletes a
    ticket** from a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.ticket.delete')


def trac_ticket_new(config, message):
    """ Fedora Hosted: Created a new ticket on a trac instance

    Adding this rule will get you notifications when a user **creates a
    ticket** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.ticket.new')


def trac_ticket_update(config, message):
    """ Fedora Hosted: Updated a ticket on a trac instance

    Adding this rule will get you notifications when a user **updates a
    ticket** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.ticket.update')


def trac_wiki_page_delete(config, message):
    """ Fedora Hosted: Deleted a wiki page of a trac instance

    Adding this rule will get you notifications when a user **deletes a wiki
    page** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.wiki.page.delete')


def trac_wiki_page_new(config, message):
    """ Fedora Hosted: Created a wiki page of a trac instance

    Adding this rule will get you notifications when a user **creates a wiki
    page** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.wiki.page.new')


def trac_wiki_page_rename(config, message):
    """ Fedora Hosted: Renamed a wiki page of a trac instance

    Adding this rule will get you notifications when a user **renames a wiki
    page** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.wiki.page.rename')


def trac_wiki_page_update(config, message):
    """ Fedora Hosted: Updated a wiki page of a trac instance

    Adding this rule will get you notifications when a user **updates a wiki
    page** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.wiki.page.update')


def trac_wiki_page_version_delete(config, message):
    """ Fedora Hosted: Deleted a version of a wiki page

    Adding this rule will get you notifications when a user **deletes a version
    of a wiki page** on a `fedorahosted <https://fedorahosted.org>`_ trac
    instance.
    """
    return message['topic'].endswith('trac.wiki.page.version.delete')
