# Generic filters for FMN
import fedmsg

import fmn.lib.pkgdb


def user_filter(config, message, fasnick=None, *args, **kw):
    """ All messages of user

    Use this filter to filter out messages that are associated with a
    specified user.
    """

    fasnick = kw.get('fasnick', fasnick)
    if fasnick:
        return fasnick in fedmsg.meta.msg2usernames(message)


def user_package_filter(config, message, fasnick=None, *args, **kw):
    """ All messages concerning user's packages

    This filter filters out messages that related to packages where the
    specified user has **commit** ACLs.
    """

    fasnick = kw.get('fasnick', fasnick)
    if fasnick:
        packages = fmn.lib.pkgdb.get_packages_of_user(fasnick)
        return packages.intersection(fedmsg.meta.msg2packages(message))
