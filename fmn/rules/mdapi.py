from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('mdapi.repo.update')])
def mdapi_repo_update(config, message):
    """ mdapi repository changes

    We have a fancy (new in 2015) service called `mdapi
    <https://apps.fedoraproject.org/mdapi>`_ which provides a JSON api over the
    yum/dnf repos we create and serve.  It updates its cache with a cronjob,
    and that cronjob produces fedmsg messages about what changed with each new
    import.

    Include this rule to receive notifications of mdapi repo changes.  Hint: it
    is nice to use in combination with rules that target packages of interest.
    """
    return message['topic'] == _('mdapi.repo.update')
