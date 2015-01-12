from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['trac'])
def trac_catchall(config, message):
    """ All Fedora Hosted activity

    Adding this rule will indiscriminately match notifications of all types
    from `fedorahosted <https://fedorahosted.org>`_.
    """
    return message['topic'].split('.')[3] == 'trac'


@hint(topics=[_('trac.git.receive')])
def trac_git_receive(config, message):
    """ Git pushes (fedorahosted.org)

    Adding this rule will get you notifications when a user **pushes commits**
    to a `fedorahosted <https://fedorahosted.org>`_ git repository.
    """
    return message['topic'].endswith('trac.git.receive')


@hint(topics=[_('trac.ticket.delete')])
def trac_ticket_delete(config, message):
    """ Deleted trac tickets (fedorahosted.org)

    Adding this rule will get you notifications when a user **deletes a
    ticket** from a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.ticket.delete')


@hint(topics=[_('trac.ticket.new')])
def trac_ticket_new(config, message):
    """ New trac tickets (fedorahosted.org)

    Adding this rule will get you notifications when a user **creates a
    ticket** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.ticket.new')


@hint(topics=[_('trac.ticket.update')])
def trac_ticket_update(config, message):
    """ Updates to trac tickets (fedorahosted.org)

    Adding this rule will get you notifications when a user **updates a
    ticket** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.ticket.update')


@hint(topics=[_('trac.wiki.page.delete')])
def trac_wiki_page_delete(config, message):
    """ Deleted pages from trac wikis (fedorahosted.org)

    Adding this rule will get you notifications when a user **deletes a wiki
    page** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.wiki.page.delete')


@hint(topics=[_('trac.wiki.page.new')])
def trac_wiki_page_new(config, message):
    """ New pages on trac wikis (fedorahosted.org)

    Adding this rule will get you notifications when a user **creates a wiki
    page** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.wiki.page.new')


@hint(topics=[_('trac.wiki.page.rename')])
def trac_wiki_page_rename(config, message):
    """ Renames of trac wiki pages (fedorahosted.org)

    Adding this rule will get you notifications when a user **renames a wiki
    page** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.wiki.page.rename')


@hint(topics=[_('trac.wiki.page.update')])
def trac_wiki_page_update(config, message):
    """ Updates to trac wiki pages (fedorahosted.org)

    Adding this rule will get you notifications when a user **updates a wiki
    page** on a `fedorahosted <https://fedorahosted.org>`_ trac instance.
    """
    return message['topic'].endswith('trac.wiki.page.update')


@hint(topics=[_('trac.wiki.page.version.delete')])
def trac_wiki_page_version_delete(config, message):
    """ Old version of trac wiki pages are deleted (fedorahosted.org)

    Adding this rule will get you notifications when a user **deletes a version
    of a wiki page** on a `fedorahosted <https://fedorahosted.org>`_ trac
    instance.
    """
    return message['topic'].endswith('trac.wiki.page.version.delete')
