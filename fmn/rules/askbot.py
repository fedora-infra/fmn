

def askbot_post_deleted(config, message):
    """ Ask: post deleted

    This rule will let through messages that get sent when either
    a question or an answer are **deleted** from the `Ask Fedora
    <https://ask.fedoraproject.org/questions>`_ forum system.
    """
    return message['topic'].endswith('askbot.post.delete')


def askbot_post_edited(config, message):
    """ Ask: post edited

    This rule will let through messages that get sent when either
    a question or an answer are **edited** on the `Ask Fedora
    <https://ask.fedoraproject.org/questions>`_ forum system.
    """
    return message['topic'].endswith('askbot.post.edit')


def askbot_post_flagged_offensive(config, message):
    """ Ask: post flagged as offensive

    Sometimes, people are rude.  This rule will let you get notified whenever
    a post is **flagged as offensive** on the `Ask Fedora
    <https://ask.fedoraproject.org/questions>`_ forum system.
    """
    return message['topic'].endswith('askbot.post.flag_offensive.add')


def askbot_post_unflagged_offensive(config, message):
    """ Ask: post unflagged as offensive

    Sometimes, people are rude.  This rule will let you get notified whenever
    a post is **unflagged as offensive** on the `Ask Fedora
    <https://ask.fedoraproject.org/questions>`_ forum system.
    """
    return message['topic'].endswith('askbot.post.flag_offensive.delete')


def askbot_tag_update(config, message):
    """ Ask: tag update

    This rule lets through messages indicating that **tags** on an
    `Ask Fedora <https://ask.fedoraproject.org/questions>`_ post have been
    modified.
    """
    return message['topic'].endswith('askbot.tag.update')
