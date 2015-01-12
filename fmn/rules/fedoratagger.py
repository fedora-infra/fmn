from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['fedoratagger'])
def fedoratagger_catchall(config, message):
    """ All Fedora Tagger events

    Adding this rule will indiscriminately match notifications of all types
    from `fedora-tagger <https://apps.fedoraproject.org/tagger>`_, i.e. votes
    on tags, usage count changes, etc..
    """
    return message['topic'].split('.')[3] == 'fedoratagger'


@hint(topics=[_('fedoratagger.rating.update')])
def fedoratagger_rating_update(config, message):
    """ The rating changes on a package (fedora-tagger)

    Adding this rule to your filters will let through messages
    from `Fedora Tagger <https://apps.fedoraproject.org/tagger>`_
    that get published when a user updates the **rating** on a package.
    """
    return message['topic'].endswith('fedoratagger.rating.update')


@hint(topics=[_('fedoratagger.tag.create')])
def fedoratagger_tag_create(config, message):
    """ New tags on a package (fedora-tagger)

    Adding this rule to your filters will let through messages
    from `Fedora Tagger <https://apps.fedoraproject.org/tagger>`_
    that get published when a user adds a **new tag** to a package.
    """
    return message['topic'].endswith('fedoratagger.tag.create')


@hint(topics=[_('fedoratagger.tag.update')])
def fedoratagger_tag_update(config, message):
    """ Votes on a package tag (fedora-tagger)

    Adding this rule to your filters will let through messages
    from `Fedora Tagger <https://apps.fedoraproject.org/tagger>`_
    that get published when a user **votes on an existing tag**.
    """
    return message['topic'].endswith('fedoratagger.tag.update')


@hint(topics=[_('fedoratagger.usage.toggle')])
def fedoratagger_usage_toggle(config, message):
    """ Usage counts change on a package (fedora-tagger)

    Adding this rule to your filters will let through messages
    from `Fedora Tagger <https://apps.fedoraproject.org/tagger>`_
    that get published when a user **toggles their usage status for a
    package**.
    """
    return message['topic'].endswith('fedoratagger.usage.toggle')


@hint(topics=[_('fedoratagger.user.rank.update')])
def fedoratagger_user_rank_update(config, message):
    """ Leaderboard changes (fedora-tagger)

    Adding this rule to your filters will let through messages
    from `Fedora Tagger <https://apps.fedoraproject.org/tagger>`_
    that get published when a user **rank gets updated**.
    """
    return message['topic'].endswith('fedoratagger.user.rank.update')
