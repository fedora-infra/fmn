from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('wiki.article.edit')])
def wiki_article_edit(config, message):
    """ Wiki edits

    Fedora's `Wiki <https://fedoraproject.org/wiki>`_ has a fedmsg hook
    that publishes messages when a user **edits a page**.  Adding this rule
    will trigger notifications whenever that event occurs.
    """
    return message['topic'].endswith('wiki.article.edit')


@hint(topics=[_('wiki.upload.complete')])
def wiki_upload_complete(config, message):
    """ Wiki media uploads

    Fedora's `Wiki <https://fedoraproject.org/wiki>`_ has a fedmsg hook
    that publishes messages when a user **uploads some media** (like a video or
    a picture).  Adding this rule will trigger notifications whenever that
    event occurs.
    """
    return message['topic'].endswith('wiki.upload.complete')
