from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['ansible'])
def all_ansible(config, message):
    """ An ansible action from Fedora-Infra

    The `Fedora Infrastructure team
    <https://fedoraproject.org/wiki/Infrastructure>`_ uses `ansible
    <http://ansibleworks.com>`_ to manage resources and deploy services.
    This rule will let through messages *all* the messages related to ansible.
    """
    return '.ansible.' in message['topic']


@hint(topics=[_('ansible.playbook.complete')])
def playbook_complete(config, message):
    """ Fedora-infra playbook runs finishing

    The `Fedora Infrastructure team
    <https://fedoraproject.org/wiki/Infrastructure>`_ uses `ansible
    <http://ansibleworks.com>`_ to manage resources and deploy services.
    This rule will let through messages indicating that a playbook run has
    *completed*.
    """
    return message['topic'].endswith('ansible.playbook.complete')


@hint(topics=[_('ansible.playbook.start')])
def playbook_started(config, message):
    """ Fedora-infra playbook runs starting

    The `Fedora Infrastructure team
    <https://fedoraproject.org/wiki/Infrastructure>`_ uses `ansible
    <http://ansibleworks.com>`_ to manage resources and deploy services.
    This rule will let through messages indicating that a playbook run has
    *started*.
    """
    return message['topic'].endswith('ansible.playbook.start')
