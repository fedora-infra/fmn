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


def trac_hosted_filter(config, message, project=None, *args, **kw):
    """ Filter the messages for a specified fedorahosted project

     Adding this rule allows you to get notifications for a specific
     `fedorahosted <https://fedorahosted.org>`_ project.
     """
    project = kw.get('project', project)
    link = fedmsg.meta.msg2link(message, **config)
    if not link:
        return False

    if ',' in project:
        project = project.split(',')
    else:
        project = [project]

    valid = False
    for proj in project:
        valid = '://fedorahosted.org/%s/' % proj in link

    return valid
