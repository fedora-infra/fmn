from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['askbot'])
def askbot_catchall(config, message):
    """ All askbot events

    Adding this rule will indiscriminately match notifications of all types
    from `Ask Fedora <https://ask.fedoraproject.org>`_ i.e.
    answers to questions, tag changes, moderation flags, etc..
    """
    return message['topic'].split('.')[3] == 'askbot'


@hint(topics=[_('askbot.post.delete')])
def askbot_post_deleted(config, message):
    """ Deleted Ask Fedora posts

    This rule will let through messages that get sent when either
    a question or an answer are **deleted** from the `Ask Fedora
    <https://ask.fedoraproject.org/questions>`_ forum system.
    """
    return message['topic'].endswith('askbot.post.delete')


@hint(topics=[_('askbot.post.edit')])
def askbot_post_edited(config, message):
    """ Updates to Ask Fedora posts

    This rule will let through messages that get sent when either
    a question or an answer are **edited** on the `Ask Fedora
    <https://ask.fedoraproject.org/questions>`_ forum system.
    """
    return message['topic'].endswith('askbot.post.edit')


@hint(topics=[_('askbot.post.flag_offensive.add')])
def askbot_post_flagged_offensive(config, message):
    """ When Ask Fedora posts are flagged as 'offensive'

    Sometimes, people are rude.  This rule will let you get notified whenever
    a post is **flagged as offensive** on the `Ask Fedora
    <https://ask.fedoraproject.org/questions>`_ forum system.
    """
    return message['topic'].endswith('askbot.post.flag_offensive.add')


@hint(topics=[_('askbot.post.flag_offensive.delete')])
def askbot_post_unflagged_offensive(config, message):
    """ When Ask Fedora posts are unflagged as 'offensive'

    Sometimes, people are rude.  This rule will let you get notified whenever
    a post is **unflagged as offensive** on the `Ask Fedora
    <https://ask.fedoraproject.org/questions>`_ forum system.
    """
    return message['topic'].endswith('askbot.post.flag_offensive.delete')


@hint(topics=[_('askbot.tag.update')])
def askbot_tag_update(config, message):
    """ Tags altered on Ask Fedora posts

    This rule lets through messages indicating that **tags** on an
    `Ask Fedora <https://ask.fedoraproject.org/questions>`_ post have been
    modified.
    """
    return message['topic'].endswith('askbot.tag.update')
