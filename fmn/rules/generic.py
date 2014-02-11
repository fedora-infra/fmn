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


def not_user_filter(config, message, fasnick=None, *args, **kw):
    """ All messages not concerning one or more users

    Use this rule to exclude messages that are associated with one or more
    users. Specify several users by separating them with a comma ','.
    """

    fasnick = kw.get('fasnick', fasnick)
    if not fasnick:
        return False

    fasnick = fasnick.split(',')
    valid = False
    for nick in fasnick:
        if nick.strip() in fedmsg.meta.msg2usernames(message, **config):
            valid = True
            break

    return valid


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


def trac_hosted_filter(config, message, project=None, *args, **kw):
    """ Filter the messages for a specified fedorahosted project

     Adding this rule allows you to get notifications for one or more
     `fedorahosted <https://fedorahosted.org>`_ project. Specify multiple
     projects by separating them with a comma ','.
     """
    project = kw.get('project', project)
    link = fedmsg.meta.msg2link(message, **config)
    if not link:
        return False

    project = project.split(',')

    valid = False
    for proj in project:
        if '://fedorahosted.org/%s/' % proj in link:
            valid = True

    return valid
