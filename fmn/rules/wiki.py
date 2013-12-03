def wiki_article_edit(config, message):
    """ Wiki: A user edited a wiki page

    Fedora's `Wiki <https://fedoraproject.org/wiki>`_ has a fedmsg hook
    that publishes messages when a user **edits a page**.  Adding this rule
    will trigger notifications whenever that event occurs.
    """
    return message['topic'].endswith('wiki.article.edit')


def wiki_upload_complete(config, message):
    """ Wiki: A user uploaded content on the wiki

    Fedora's `Wiki <https://fedoraproject.org/wiki>`_ has a fedmsg hook
    that publishes messages when a user **uploads some media** (like a video or
    a picture).  Adding this rule will trigger notifications whenever that
    event occurs.
    """
    return message['topic'].endswith('wiki.upload.complete')
