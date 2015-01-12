from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('fedbadges.badge.award')])
def fedbadges_badge_award(config, message):
    """ New badge awards in the Fedora Badges system

    Adding this rule will let through notifications from the `Fedora Badges
    <https://badges.fedoraproject.org>`_ system whenever someone is *awarded a
    new badge*.
    """
    return message['topic'].endswith('fedbadges.badge.award')


@hint(topics=[_('fedbadges.person.login.first')])
def fedbadges_person_first_login(config, message):
    """ New people login to badges.fedoraproject.org

    Adding this rule will let through notifications from the `Fedora Badges
    <https://badges.fedoraproject.org>`_ system whenever someone *logs in*
    for the *first time*.
    """
    return message['topic'].endswith('fedbadges.person.login.first')


@hint(topics=[_('fedbadges.person.rank.advance')])
def fedbadges_person_rank_advance(config, message):
    """ Rank changes in the Fedora Badges system

    Adding this rule will let through notifications from the `Fedora Badges
    <https://badges.fedoraproject.org>`_ system whenever someone's *rank
    changes* (presumably after they've been awarded a new badge).
    """
    return message['topic'].endswith('fedbadges.person.rank.advance')
