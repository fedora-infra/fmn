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


def fedoratagger_usage_toggle(config, message):
    """ Tagger: Someone marked that they use a package

    Adding this rule to your filters will let through messages
    from `Fedora Tagger <https://apps.fedoraproject.org/tagger>`_
    that get published when a user **toggles their usage status for a
    package**.
    """
    return message['topic'].endswith('fedoratagger.usage.toggle')


def fedoratagger_user_rank_update(config, message):
    """ Tagger: Rank of an user in Fedora Tagger leaderboard was changed

    Adding this rule to your filters will let through messages
    from `Fedora Tagger <https://apps.fedoraproject.org/tagger>`_
    that get published when a user **rank gets updated**.
    """
    return message['topic'].endswith('fedoratagger.user.rank.update')


