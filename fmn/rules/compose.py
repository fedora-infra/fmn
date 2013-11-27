def compose_branched_complete(config, message):
    """ Compose: Compose completed for a specific branch

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.branched.complete')


def compose_branched_mash_complete(config, message):
    """ Compose: Mash completed for a specific branch

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.branched.mash.complete')


def compose_branched_mash_start(config, message):
    """ Compose: Mash started for a specific branch

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.branched.mash.start')


def compose_branched_pungify_complete(config, message):
    """ Compose: Pungi completed for a specific branch

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.branched.pungify.complete')


def compose_branched_pungify_start(config, message):
    """ Compose: Pungi started for a specific branch

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.branched.pungify.start')


def compose_branched_rsync_complete(config, message):
    """ Compose: rsync completed for a specific branch

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.branched.rsync.complete')


def compose_branched_rsync_start(config, message):
    """ Compose: rsync started for a specific branch

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.branched.rsync.start')


def compose_branched_start(config, message):
    """ Compose: Compose started for a specific branch

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.branched.start')


def compose_rawhide_complete(config, message):
    """ Compose: Compose completed for rawhide

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.rawhide.complete')


def compose_rawhide_mash_complete(config, message):
    """ Compose: Mash completed for rawhide

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.rawhide.mash.complete')

def compose_rawhide_mash_start(config, message):
    """ Compose: Mash started for rawhide

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.rawhide.mash.start')


def compose_rawhide_rsync_complete(config, message):
    """ Compose:

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.rawhide.rsync.complete')


def compose_rawhide_rsync_start(config, message):
    """ Compose: rsync started for rawhide

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.rawhide.rsync.start')


def compose_rawhide_start(config, message):
    """ Compose: Compose started for rawhide

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('compose.rawhide.start')
