def fedbadges_badge_award(config, message):
    """ Badges: A new badge has been awarded to someone

    Adding this rule will let through notifications from the `Fedora Badges
    <https://badges.fedoraproject.org>`_ system whenever someone is *awarded a
    new badge*.
    """
    return message['topic'].endswith('fedbadges.badge.award')


def fedbadges_person_rank_advance(config, message):
    """ Badges: The rank of someone changed on the badges leaderboard

    Adding this rule will let through notifications from the `Fedora Badges
    <https://badges.fedoraproject.org>`_ system whenever someone's *rank
    changes* (presumably after they've been awarded a new badge).
    """
    return message['topic'].endswith('fedbadges.person.rank.advance')
