# Generic rules for FMN
import re

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

    fasnick = fasnick or [] and fasnick.split(',')
    valid = True
    for nick in fasnick:
        if nick.strip() in fedmsg.meta.msg2usernames(message, **config):
            valid = False
            break

    return valid


def user_package_filter(config, message, fasnick=None, *args, **kw):
    """ All messages concerning user's packages

    This rule includes messages that relate to packages where the
    specified user has **commit** ACLs.
    """

    fasnick = kw.get('fasnick', fasnick)
    if fasnick:
        packages = fmn.rules.utils.get_packages_of_user(config, fasnick)
        msg_packages = fedmsg.meta.msg2packages(message, **config)
        return packages.intersection(msg_packages)

    return False


def package_filter(config, message, package=None, *args, **kw):
    """ All messages pertaining to a certain package

    Use this rule to include messages that relate to a certain package
    (*i.e., nethack*).
    """

    package = kw.get('package', package)
    if package:
        return package in fedmsg.meta.msg2packages(message, **config)


def package_regex_filter(config, message, pattern=None, *args, **kw):
    """ All messages pertaining to packages matching a given regex

    Use this rule to include messages that relate to packages that match
    particular regular expressions
    (*i.e., (maven|javapackages-tools|maven-surefire)*).
    """

    pattern = kw.get('pattern', pattern)
    if pattern:
        packages = fedmsg.meta.msg2packages(message, **config)
        regex = re.compile(pattern)
        return any([regex.match(package) for package in packages])


def regex_filter(config, message, pattern=None, *args, **kw):
    """ All messages matching a given regex

    Use this rule to include messages that bear a certain pattern.
    This can be anything that appears anywhere in the message (for instance,
    you could combine this with rules for wiki updates or Ask Fedora changes
    to alert yourself of activity in your area of expertise).

    (*i.e., (beefy miracle)*).
    """

    pattern = kw.get('pattern', pattern)
    if pattern:
        regex = re.compile(pattern)
        return bool(regex.match(json.dumps(message)))


def trac_hosted_filter(config, message, project=None, *args, **kw):
    """ Filter the messages for one or more fedorahosted projects

     Adding this rule allows you to get notifications for one or more
     `fedorahosted <https://fedorahosted.org>`_ project. Specify multiple
     projects by separating them with a comma ','.
     """
    project = kw.get('project', project)
    link = fedmsg.meta.msg2link(message, **config)
    if not link:
        return False

    project = project or [] and project.split(',')

    valid = False
    for proj in project:
        if '://fedorahosted.org/%s/' % proj.strip() in link:
            valid = True

    return valid
