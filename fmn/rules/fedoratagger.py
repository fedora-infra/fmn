def fedoratagger_rating_update(config, message):
    """ Tagger: The rating of a package has been updated

    Adding this rule to your filters will let through messages
    from `Fedora Tagger <https://apps.fedoraproject.org/tagger>`_
    that get published when a user updates the **rating** on a package.
    """
    return message['topic'].endswith('fedoratagger.rating.update')


def fedoratagger_tag_create(config, message):
    """ Tagger: A new tag has been added to a package

    Adding this rule to your filters will let through messages
    from `Fedora Tagger <https://apps.fedoraproject.org/tagger>`_
    that get published when a user adds a **new tag** to a package.
    """
    return message['topic'].endswith('fedoratagger.tag.create')


def fedoratagger_tag_update(config, message):
    """ Tagger: Someone voted on a tag

    Adding this rule to your filters will let through messages
    from `Fedora Tagger <https://apps.fedoraproject.org/tagger>`_
    that get published when a user **votes on an existing tag**.
    """
    return message['topic'].endswith('fedoratagger.tag.update')
