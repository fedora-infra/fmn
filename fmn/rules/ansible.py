from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('ansible.playbook.complete')])
def playbook_complete(config, message):
    """ Ansible playbook completed

    The `Fedora Infrastructure team
    <https://fedoraproject.org/wiki/Infrastructure>`_ uses `ansible
    <http://ansibleworks.com>`_ to manage resources and deploy services.
    This rule will let through messages indicating that a playbook run has
    *completed*.
    """
    return message['topic'].endswith('ansible.playbook.complete')


@hint(topics=[_('ansible.playbook.start')])
def playbook_started(config, message):
    """ Ansible playbook started

    The `Fedora Infrastructure team
    <https://fedoraproject.org/wiki/Infrastructure>`_ uses `ansible
    <http://ansibleworks.com>`_ to manage resources and deploy services.
    This rule will let through messages indicating that a playbook run has
    *started*.
    """
    return message['topic'].endswith('ansible.playbook.start')
