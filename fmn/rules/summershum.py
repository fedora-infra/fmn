from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['summershum'])
def summershum_catchall(config, message):
    """ All summershum events

    Adding this rule will indiscriminately match notifications of all types
    from `summershum <https://github.com/fedora-infra/summershum>`_, a backend
    service that tracks the md5 and sha sums of the contents of new upstream
    tarballs.
    """
    return message['topic'].split('.')[3] == 'summershum'


@hint(topics=[_('summershum.ingest.start')])
def summershum_ingest_start(config, message):
    """ Summershum starts ingesting a tarball

    Adding this rule to your filters will let through messages
    from `summershum <https://github.com/fedora-infra/summershum>`_
    when it starts working on a newly uploaded tarball.
    """
    return message['topic'].endswith('summershum.ingest.start')


@hint(topics=[_('summershum.ingest.fail')])
def summershum_ingest_fail(config, message):
    """ Summershum fails to ingest a tarball

    Adding this rule to your filters will let through messages
    from `summershum <https://github.com/fedora-infra/summershum>`_
    when it fails somehow on a newly uploaded tarball.
    """
    return message['topic'].endswith('summershum.ingest.fail')


@hint(topics=[_('summershum.ingest.complete')])
def summershum_ingest_complete(config, message):
    """ Summershum finishes ingesting a tarball

    Adding this rule to your filters will let through messages
    from `summershum <https://github.com/fedora-infra/summershum>`_
    when it finishing pulling in a newly uploaded tarball.
    """
    return message['topic'].endswith('summershum.ingest.complete')
