def fedbadges_badge_award(config, message):
    """ Fedbadges: A new badge has been awarded to someone

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fedbadges.badge.award')


def fedbadges_person_rank_advance(config, message):
    """ Fedbadges: The rank of someone changed in the leaderboard of badges

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fedbadges.person.rank.advance')
