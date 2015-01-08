def summershum_ingest_start(config, message):
    """ Summershum: Started ingesting a tarball

    Adding this rule to your filters will let through messages
    from `summershum <https://github.com/fedora-infra/summershum>`_
    when it starts working on a newly uploaded tarball.
    """
    return message['topic'].endswith('summershum.ingest.start')

def summershum_ingest_fail(config, message):
    """ Summershum: failed to ingest a tarball

    Adding this rule to your filters will let through messages
    from `summershum <https://github.com/fedora-infra/summershum>`_
    when it fails somehow on a newly uploaded tarball.
    """
    return message['topic'].endswith('summershum.ingest.fail')

def summershum_ingest_complete(config, message):
    """ Summershum: finished ingesting a tarball

    Adding this rule to your filters will let through messages
    from `summershum <https://github.com/fedora-infra/summershum>`_
    when it finishing pulling in a newly uploaded tarball.
    """
    return message['topic'].endswith('summershum.ingest.complete')
