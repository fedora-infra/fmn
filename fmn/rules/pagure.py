from fmn.lib.hinting import hint, prefixed as _

import fedmsg.meta


@hint(categories=['pagure'])
def pagure_catchall(config, message):
    """ All pagure.io activity

    Adding this rule will indiscriminately match notifications of all types
    from `pagure <https://pagure.io>`_ (but only the repositories that have the
    fedmsg hook enabled).
    """
    return message['topic'].split('.')[3] == 'pagure'


@hint(categories=['pagure'], invertible=False)
def pagure_specific_project_filter(config, message, project=None, *args, **kw):
    """ Particular pagure projects

     Adding this rule allows you to get notifications for one or more
     `pagure.io <https://pagure.io>`_ projects. Specify multiple
     projects by separating them with a comma ','.
     """

    if not pagure_catchall(config, message):
        return False

    project = kw.get('project', project)
    link = fedmsg.meta.msg2link(message, **config)
    if not link:
        return False

    project = project.split(',') if project else []

    valid = False
    for proj in project:
        if '://pagure.io/%s/' % proj.strip() in link:
            valid = True

    return valid


@hint(categories=['pagure'], invertible=False)
def pagure_specific_project_tag_filter(config, message, tags=None, *args, **kw):
    """ Particular pagure project tags

     Adding this rule allows you to get notifications for one or more
     `pagure.io <https://pagure.io>`_ projects having the specified tags.
     Specify multiple tags by separating them with a comma ','.
     """

    if not pagure_catchall(config, message):
        return False

    tags = tags.split(',') if tags else []
    tags = [tag.strip() for tag in tags if tag and tag.strip()]

    project_tags = set()
    project_tags.update(message.get('project', {}).get('tags', []))
    project_tags.update(
        message.get('pullrequest', {}).get('project', {}).get('tags', []))
    project_tags.update(
        message.get('commit', {}).get('repo', {}).get('tags', []))

    valid = len(project_tags.intersection(set(tags))) > 0

    return valid


@hint(topics=[_('pagure.project.new', prefix='io.pagure')])
def pagure_project_new(config, message):
    """ New pagure projects

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **a new project is added**.
    """
    return message['topic'].endswith('pagure.project.new')


@hint(topics=[_('pagure.issue.new', prefix='io.pagure')])
def pagure_issue_new(config, message):
    """ New pagure issues

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **new issues are filed**.
    """
    return message['topic'].endswith('pagure.issue.new')


@hint(topics=[_('pagure.issue.comment.added', prefix='io.pagure')])
def pagure_issue_comment_added(config, message):
    """ Comments on pagure issues

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **comments are added to
    issues**.
    """
    return message['topic'].endswith('pagure.issue.comment.added')


@hint(topics=[_('pagure.issue.tag.added', prefix='io.pagure')])
def pagure_issue_tag_added(config, message):
    """ Tags added to pagure issues

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **tags are added to issues**.
    """
    return message['topic'].endswith('pagure.issue.tag.added')


@hint(topics=[_('pagure.issue.tag.removed', prefix='io.pagure')])
def pagure_issue_tag_removed(config, message):
    """ Tags removed from pagure issues

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **tags are removed from
    issues**.
    """
    return message['topic'].endswith('pagure.issue.tag.removed')


@hint(topics=[_('pagure.issue.assigned.added', prefix='io.pagure')])
def pagure_issue_assigned_added(config, message):
    """ Someone is assigned to a pagure issue

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **someone is assigned
    to an issue**.
    """
    return message['topic'].endswith('pagure.issue.assigned.added')


@hint(topics=[_('pagure.issue.assigned.reset', prefix='io.pagure')])
def pagure_issue_assigned_reset(config, message):
    """ The assignment on a pagure issue is reset

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **the assignment on
    an issue is reset**.
    """
    return message['topic'].endswith('pagure.issue.assigned.reset')


@hint(topics=[_('pagure.issue.dependency.added', prefix='io.pagure')])
def pagure_issue_dependency_added(config, message):
    """ A dep was added to a pagure issue

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **a dependency is added to a
    pagure issue**.
    """
    return message['topic'].endswith('pagure.issue.dependency.added')


@hint(topics=[_('pagure.issue.dependency.removed', prefix='io.pagure')])
def pagure_issue_dependency_removed(config, message):
    """ A dep was removed from a pagure issue

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **a dependency is removed
    from a pagure issue**.
    """
    return message['topic'].endswith('pagure.issue.dependency.removed')


@hint(topics=[_('pagure.issue.edit', prefix='io.pagure')])
def pagure_issue_edit(config, message):
    """ Issues being edited

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **issues are edited**.
    """
    return message['topic'].endswith('pagure.issue.edit')


@hint(topics=[_('pagure.project.edit', prefix='io.pagure')])
def pagure_project_edit(config, message):
    """ Projects being edited

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **project details are edited**.
    """
    return message['topic'].endswith('pagure.project.edit')


@hint(topics=[_('pagure.project.user.added', prefix='io.pagure')])
def pagure_project_user_added(config, message):
    """ New users added to a project

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **a new user is added to a
    project**.
    """
    return message['topic'].endswith('pagure.project.user.added')


@hint(topics=[_('pagure.project.tag.removed', prefix='io.pagure')])
def pagure_project_tag_removed(config, message):
    """ Tags removed from a project

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **a tags are removed from a
    project**.

    """
    return message['topic'].endswith('pagure.project.tag.removed')


@hint(topics=[_('pagure.project.tag.edited', prefix='io.pagure')])
def pagure_project_tag_edited(config, message):
    """ Tags edited on a project

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **a project's tags are edited**.
    """
    return message['topic'].endswith('pagure.project.tag.edited')


@hint(topics=[_('pagure.project.forked', prefix='io.pagure')])
def pagure_project_forked(config, message):
    """ A project is forked

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **a project is forked**.
    """
    return message['topic'].endswith('pagure.project.forked')


@hint(topics=[_('pagure.pull-request.comment.added', prefix='io.pagure')])
def pagure_pull_request_comment_added(config, message):
    """ Comments on pull requests

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **there's a new comment on a
    pull-request**.
    """
    return message['topic'].endswith('pagure.pull-request.comment.added')


@hint(topics=[_('pagure.pull-request.closed', prefix='io.pagure')])
def pagure_pull_request_closed(config, message):
    """ A pull request is closed

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **a pull request is closed**.
    """
    return message['topic'].endswith('pagure.pull-request.closed')


@hint(topics=[_('pagure.pull-request.new', prefix='io.pagure')])
def pagure_pull_request_new(config, message):
    """ A pull request is created

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **a pull request is opened**.
    """
    return message['topic'].endswith('pagure.pull-request.new')


@hint(topics=[_('pagure.pull-request.flag.added', prefix='io.pagure')])
def pagure_pull_request_flag_added(config, message):
    """ A flag is added to a pull request

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **a flag is added to a pull
    request**.  These are continuous-integration status updates.
    """
    return message['topic'].endswith('pagure.pull-request.flag.added')


@hint(topics=[_('pagure.pull-request.flag.updated', prefix='io.pagure')])
def pagure_pull_request_flag_updated(config, message):
    """ A flag is updated on a pull request

    Adding this rule to your filters will let through messages
    from `pagure.io <https://pagure.io>`_ when **a flag is updated on a pull
    request**.  These are continuous-integration status updates.
    """
    return message['topic'].endswith('pagure.pull-request.flag.updated')
