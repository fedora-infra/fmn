from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['faf'])
def faf_catchall(config, message):
    """ All FAF (ABRT server) events

    Adding this rule will indiscriminately match notifications of all types
    from `faf <https://retrace.fedoraproject.org>`_, i.e. new and often
    occurring crash reports and problems.
    """
    return message['topic'].split('.')[3] == 'faf'


# Reports

@hint(topics=[_('faf.report.threshold1')])
def faf_report_threshold1(config, message):
    """ New report

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a new crash report appears.  Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.report.threshold1')


@hint(topics=[_('faf.report.threshold10')])
def faf_report_threshold10(config, message):
    """ A report reaches 10 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash report reaches 10 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.report.threshold10')


@hint(topics=[_('faf.report.threshold100')])
def faf_report_threshold100(config, message):
    """ A report reaches 100 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash report reaches 100 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.report.threshold100')


@hint(topics=[_('faf.report.threshold1000')])
def faf_report_threshold1000(config, message):
    """ A report reaches 1 000 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash report reaches 1 000 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.report.threshold1000')


@hint(topics=[_('faf.report.threshold10000')])
def faf_report_threshold10000(config, message):
    """ A report reaches 10 000 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash report reaches 10 000 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.report.threshold10000')


@hint(topics=[_('faf.report.threshold100000')])
def faf_report_threshold100000(config, message):
    """ A report reaches 100 000 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash report reaches 100 000 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.report.threshold100000')


@hint(topics=[_('faf.report.threshold1000000')])
def faf_report_threshold1000000(config, message):
    """ A report reaches 1 000 000 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash report reaches 1 000 000 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.report.threshold1000000')


# Problems

@hint(topics=[_('faf.problem.threshold1')])
def faf_problem_threshold1(config, message):
    """ New problem

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a new problem (cluster of similar crash reports) appears.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.problem.threshold1')


@hint(topics=[_('faf.problem.threshold10')])
def faf_problem_threshold10(config, message):
    """ A problem reaches 10 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash problem (cluster of similar crash reports) reaches 10 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.problem.threshold10')


@hint(topics=[_('faf.problem.threshold100')])
def faf_problem_threshold100(config, message):
    """ A problem reaches 100 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash problem (cluster of similar crash reports) reaches 100 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.problem.threshold100')


@hint(topics=[_('faf.problem.threshold1000')])
def faf_problem_threshold1000(config, message):
    """ A problem reaches 1 000 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash problem (cluster of similar crash reports) reaches 1 000 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.problem.threshold1000')


@hint(topics=[_('faf.problem.threshold10000')])
def faf_problem_threshold10000(config, message):
    """ A problem reaches 10 000 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash problem (cluster of similar crash reports) reaches 10 000 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.problem.threshold10000')


@hint(topics=[_('faf.problem.threshold100000')])
def faf_problem_threshold100000(config, message):
    """ A problem reaches 100 000 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash problem (cluster of similar crash reports) reaches 100 000 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.problem.threshold100000')


@hint(topics=[_('faf.problem.threshold1000000')])
def faf_problem_threshold1000000(config, message):
    """ A problem reaches 1 000 000 occurrences

    `FAF (ABRT server) <https://retrace.fedoraproject.org/>`_ publishes messages
    when a crash problem (cluster of similar crash reports) reaches 1 000 000 occurrences.
    Adding this rule will get you those messages.
    """
    return message['topic'].endswith('faf.problem.threshold1000000')
