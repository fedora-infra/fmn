# Generic rules for FMN
import fedmsg

import fmn.rules.utils


def user_filter(config, message, fasnick=None, *args, **kw):
    """ All messages for a certain user

    Use this rule to include messages that are associated with a
    specific user.
    """

    fasnick = kw.get('fasnick', fasnick)
    if fasnick:
        return fasnick in fedmsg.meta.msg2usernames(message, **config)


def user_package_filter(config, message, fasnick=None, *args, **kw):
    """ All messages concerning user's packages

    This rule includes messages that relate to packages where the
    specified user has **commit** ACLs.
    """

    fasnick = kw.get('fasnick', fasnick)
    if fasnick:
        user_packages = fmn.rules.utils.get_packages_of_user(config, fasnick)
        msg_packages = fedmsg.meta.msg2packages(message, **config)
        return user_packages.intersection(msg_packages)


def package_filter(config, message, package=None, *args, **kw):
    """ All messages pertaining to a certain package

    Use this rule to include messages that relate to a certain package
    (*i.e., nethack*).
    """

    package = kw.get('package', package)
    if package:
        return package in fedmsg.meta.msg2packages(message, **config)
