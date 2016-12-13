# Generic rules for FMN

import fedmsg
import fedmsg.encoding
import fedmsg.meta

import fmn.rules.utils
from fmn.lib.hinting import hint


@hint(callable=lambda config, fasnick: dict(users=[fasnick]))
def user_filter(config, message, fasnick=None, *args, **kw):
    """ A particular user

    Use this rule to include messages that are associated with a
    specific user.
    """

    fasnick = kw.get('fasnick', fasnick)
    if fasnick:
        return fasnick in fmn.rules.utils.msg2usernames(message, **config)


@hint(callable=lambda config, fasnick: dict(not_users=[fasnick]),
      invertible=False)
def not_user_filter(config, message, fasnick=None, *args, **kw):
    """ Everything except a particular user

    Use this rule to exclude messages that are associated with one or more
    users. Specify several users by separating them with a comma ','.
    """

    fasnick = kw.get('fasnick', fasnick)
    if not fasnick:
        return False

    fasnick = (fasnick or []) and fasnick.split(',')
    valid = True
    for nick in fasnick:
        if nick.strip() in fmn.rules.utils.msg2usernames(message, **config):
            valid = False
            break

    return valid


def _get_users_of_group(config, group):
    """ Utility to query fas for users of a group. """
    if not group:
        return set()
    fas = fmn.rules.utils.get_fas(config)
    return fmn.rules.utils.get_user_of_group(config, fas, group)


@hint(callable=_get_users_of_group)
def fas_group_member_filter(config, message, group=None, *args, **kw):
    """ Messages regarding any member of a FAS group

    Use this rule to include messages that have anything to do with **any
    user** belonging to a particular fas group.  You might want to use this
    to monitor the activity of a group for which you are responsible.
    """
    if not group:
        return False
    fasusers = _get_users_of_group(config, group)
    msgusers = fmn.rules.utils.msg2usernames(message, **config)
    return bool(fasusers.intersection(msgusers))


def _user_package_filter_hint(flags):
    def hint_callable(config, fasnick):
        packages = fmn.rules.utils.get_packages_of_user(config, fasnick, flags)
        return dict(packages=packages)
    return hint_callable


all_acls = ['point of contact', 'co-maintained', 'watch']
@hint(callable=_user_package_filter_hint(all_acls))
def user_package_filter(config, message, fasnick=None, *args, **kw):
    """ A particular user's packages (any acl)

    This rule includes messages that relate to packages where the
    specified user has *either* commit ACLs or the watchcommits flag.
    """

    fasnick = kw.get('fasnick', fasnick)
    if fasnick:
        msg_packages = fmn.rules.utils.msg2packages(message, **config)
        if not msg_packages:
            # If the message has no packages associated with it, there's no
            # way that "one of them" is going to happen to belong to this user,
            # so let's not waste our time doing the somewhat expensive call out
            # to pkgdb on the next line to check.
            return False
        usr_packages = fmn.rules.utils.get_packages_of_user(
            config, fasnick, all_acls)
        return usr_packages.intersection(msg_packages)

    return False

only_commit = ['point of contact', 'co-maintained']
@hint(callable=_user_package_filter_hint(only_commit))
def user_package_commit_filter(config, message, fasnick=None, *args, **kw):
    """ A particular user's packages (commit acl)

    This rule includes messages that relate to packages where the
    specified user has commit ACLs.
    """

    fasnick = kw.get('fasnick', fasnick)
    if fasnick:
        msg_packages = fmn.rules.utils.msg2packages(message, **config)
        if not msg_packages:
            # If the message has no packages associated with it, there's no
            # way that "one of them" is going to happen to belong to this user,
            # so let's not waste our time doing the somewhat expensive call out
            # to pkgdb on the next line to check.
            return False
        usr_packages = fmn.rules.utils.get_packages_of_user(
            config, fasnick, only_commit)
        return usr_packages.intersection(msg_packages)

    return False


only_watchcommits = ['watch']
@hint(callable=_user_package_filter_hint(only_watchcommits))
def user_package_watch_filter(config, message, fasnick=None, *args, **kw):
    """ A particular user's packages (watchcommits flag)

    This rule includes messages that relate to packages where the
    specified user has the watchcommits flag set.
    """

    fasnick = kw.get('fasnick', fasnick)
    if fasnick:
        msg_packages = fmn.rules.utils.msg2packages(message, **config)
        if not msg_packages:
            # If the message has no packages associated with it, there's no
            # way that "one of them" is going to happen to belong to this user,
            # so let's not waste our time doing the somewhat expensive call out
            # to pkgdb on the next line to check.
            return False
        usr_packages = fmn.rules.utils.get_packages_of_user(
            config, fasnick, only_watchcommits)
        return usr_packages.intersection(msg_packages)

    return False


@hint(callable=lambda config, package: dict(packages=[package]))
def package_filter(config, message, package=None, *args, **kw):
    """ A particular package

    Use this rule to include messages that relate to a certain package
    (*i.e., nethack*).
    """

    package = kw.get('package', package)
    if package:
        return package in fmn.rules.utils.msg2packages(message, **config)


# Can't hint this one.  Can't pass a regex on to postgres
def package_regex_filter(config, message, pattern=None, *args, **kw):
    """ All packages matching a regular expression

    Use this rule to include messages that relate to packages that match
    particular regular expressions
    (*i.e., (maven|javapackages-tools|maven-surefire)*).
    """

    pattern = kw.get('pattern', pattern)
    if pattern:
        packages = fmn.rules.utils.msg2packages(message, **config)
        regex = fmn.rules.utils.compile_regex(pattern.encode('utf-8'))
        return any([regex.search(p.encode('utf-8')) for p in packages])


# Can't hint this one.  Can't pass a regex on to postgres
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
        regex = fmn.rules.utils.compile_regex(pattern.encode('utf-8'))
        return bool(regex.search(
            fedmsg.encoding.dumps(message['msg']).encode('utf-8')
        ))


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

    project = project.split(',') if project else []

    valid = False
    for proj in project:
        if '://fedorahosted.org/%s/' % proj.strip() in link:
            valid = True

    return valid
