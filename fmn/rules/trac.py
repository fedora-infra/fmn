def trac_git_receive(config, message):
    """ Trac: A user pushed a changed to the git repository of the trac.

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('trac.git.receive')


def trac_ticket_delete(config, message):
    """ Trac: A user deleted a ticket on the trac

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('trac.ticket.delete')


def trac_ticket_new(config, message):
    """ Trac: A user created a new ticket on the trac

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('trac.ticket.new')


def trac_ticket_update(config, message):
    """ Trac: A user updated a ticket on the trac

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('trac.ticket.update')


def trac_wiki_page_delete(config, message):
    """ Trac: A user deleted a wiki page of the trac

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('trac.wiki.page.delete')


def trac_wiki_page_new(config, message):
    """ Trac: A user created a wiki page of the trac

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('trac.wiki.page.new')


def trac_wiki_page_rename(config, message):
    """ Trac: A user renamed a wiki page of the trac

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('trac.wiki.page.rename')


def trac_wiki_page_update(config, message):
    """ Trac: A user updated a wiki page of the trac

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('trac.wiki.page.update')


def trac_wiki_page_version_delete(config, message):
    """ Trac: A user deleted a version of a wiki page of the trac

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('trac.wiki.page.version.delete')
