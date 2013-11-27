def wiki_article_edit(config, message):
    """ Wiki: A user edited a wiki page

Fedora's `Wiki <https://fedoraproject.org/wiki>`_ has a fedmsg hook
that publishes messages like this one when a user edits a page.
    """
    return message['topic'].endswith('wiki.article.edit')


def wiki_upload_complete(config, message):
    """ Wiki: A user uploaded content on the wiki

Fedora's `Wiki <https://fedoraproject.org/wiki>`_ hook also publishes
messages when a user upload some media (like a video or a picture).
    """
    return message['topic'].endswith('wiki.upload.complete')
