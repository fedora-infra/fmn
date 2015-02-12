# Generic rules for FMN

import fedmsg
import fedmsg.encoding

import fmn.rules.utils
from fmn.lib.hinting import hint


import logging
log = logging.getLogger('fedmsg')

try:
    import re2 as re
    re.set_fallback_notification(re.FALLBACK_WARNING)
except ImportError:
    log.warning("Couldn't import the 're2' module.")
    import re


def user_filter(config, message, fasnick=None, *args, **kw):
    """ A particular user

    Use this rule to include messages that are associated with a
    specific user.
    """

    fasnick = kw.get('fasnick', fasnick)
    if fasnick:
        return fasnick in fedmsg.meta.msg2usernames(message, **config)


def not_user_filter(config, message, fasnick=None, *args, **kw):
    """ Everything except a particular user

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
    """ A particular user's packages

    This rule includes messages that relate to packages where the
    specified user has **commit** ACLs.
    """

    fasnick = kw.get('fasnick', fasnick)
    if fasnick:
        msg_packages = fedmsg.meta.msg2packages(message, **config)
        if not msg_packages:
            # If the message has no packages associated with it, there's no
            # way that "one of them" is going to happen to belong to this user,
            # so let's not waste our time doing the somewhat expensive call out
            # to pkgdb on the next line to check.
            return False
        usr_packages = fmn.rules.utils.get_packages_of_user(config, fasnick)
        return usr_packages.intersection(msg_packages)

    return False


def package_filter(config, message, package=None, *args, **kw):
    """ A particular package

    Use this rule to include messages that relate to a certain package
    (*i.e., nethack*).
    """

    package = kw.get('package', package)
    if package:
        return package in fedmsg.meta.msg2packages(message, **config)


def package_regex_filter(config, message, pattern=None, *args, **kw):
    """ All packages matching a regular expression

    Use this rule to include messages that relate to packages that match
    particular regular expressions
    (*i.e., (maven|javapackages-tools|maven-surefire)*).
    """

    pattern = kw.get('pattern', pattern)
    if pattern:
        packages = fedmsg.meta.msg2packages(message, **config)
        regex = re.compile(pattern)
        return any([regex.search(package) for package in packages])


def regex_filter(config, message, pattern=None, *args, **kw):
    """ All messages matching a regular expression

    Use this rule to include messages that bear a certain pattern.
    This can be anything that appears anywhere in the message (for instance,
    you could combine this with rules for wiki updates or Ask Fedora changes
    to alert yourself of activity in your area of expertise).

    (*i.e., (beefy miracle)*).
    """

    pattern = kw.get('pattern', pattern)
    if pattern:
        regex = re.compile(pattern)
        return bool(regex.search(fedmsg.encoding.dumps(message['msg'])))


@hint(categories=['trac'], invertible=False)
def trac_hosted_filter(config, message, project=None, *args, **kw):
    """ Particular fedorahosted projects

     Adding this rule allows you to get notifications for one or more
     `fedorahosted <https://fedorahosted.org>`_ projects. Specify multiple
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
