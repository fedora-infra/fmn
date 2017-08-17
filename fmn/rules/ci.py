from fmn.lib.hinting import hint, prefixed as _

# Basic building steps

@hint(categories=['ci'])
def ci_catchall(config, message):
    """ All CI events

    Adding this rule will indiscriminately match notifications of all types
    from the `Fedora Atomic CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_, i.e.
    new build queued, running, complete, compose running, complete, etc..
    """
    return message['topic'].split('.')[3] == 'ci'


@hint(topics=[_('ci.pipeline.package.ignore')])
def ci_package_ignore(config, message):
    """ Package ignored by CI

    Adding this rule will trigger notifications a package is ignored by
    the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith('ci.pipeline.package.ignore')


@hint(topics=[_('ci.pipeline.package.queued')])
def ci_package_queued(config, message):
    """ Package queued in CI

    Adding this rule will trigger notifications a package has been queued
    to be built in Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith('ci.pipeline.package.queued')


@hint(topics=[_('ci.pipeline.package.running')])
def ci_package_running(config, message):
    """ Package building in CI

    Adding this rule will trigger notifications a package is being built
    in the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith('ci.pipeline.package.running')


@hint(topics=[_('ci.pipeline.package.complete')])
def ci_package_complete(config, message):
    """ Package built by CI

    Adding this rule will trigger notifications a package has been built by
    the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith('ci.pipeline.package.complete')


@hint(topics=[_('ci.pipeline.compose.running')])
def ci_compose_running(config, message):
    """ A compose is being built by CI

    Adding this rule will trigger notifications a compose is being built by
    the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith('ci.pipeline.compose.running')


@hint(topics=[_('ci.pipeline.compose.complete')])
def ci_compose_complete(config, message):
    """ A compose was done by CI

    Adding this rule will trigger notifications a compose has been built by
    the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith('ci.pipeline.compose.complete')


@hint(topics=[_('ci.pipeline.image.running')])
def ci_image_running(config, message):
    """ An image is being built by CI

    Adding this rule will trigger notifications an image is being built by
    the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith('ci.pipeline.image.running')


@hint(topics=[_('ci.pipeline.image.complete')])
def ci_image_complete(config, message):
    """ An image was built by CI

    Adding this rule will trigger notifications an image has been built by
    the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith('ci.pipeline.image.complete')


# Tests steps


@hint(topics=[_('ci.pipeline.package.test.functional.queued')])
def ci_package_test_queued(config, message):
    """ Functional tests queued for a package

    Adding this rule will trigger notifications when functional tests of a
    package have been queued by the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith(
        'ci.pipeline.package.test.functional.queued')


@hint(topics=[_('ci.pipeline.package.test.functional.running')])
def ci_package_test_running(config, message):
    """ Functional tests are running for a package

    Adding this rule will trigger notifications when functional tests of a
    package are running in the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith(
        'ci.pipeline.package.test.functional.running')


@hint(topics=[_('ci.pipeline.package.test.functional.complete')])
def ci_package_test_complete(config, message):
    """ Functional tests completed for a package

    Adding this rule will trigger notifications when functional tests of a
    package have completed in the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith(
        'ci.pipeline.package.test.functional.complete')


@hint(topics=[_('ci.pipeline.compose.test.integration.queued')], invertible=False)
def ci_compose_test_queued(config, message):
    """ Integration tests queued for a compose

    Adding this rule will trigger notifications when integration tests of a
    compose have been queued by the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith(
        'ci.pipeline.package.test.functional.queued')


@hint(topics=[_('ci.pipeline.compose.test.integration.running')], invertible=False)
def ci_compose_test_running(config, message):
    """ Integration tests are running for a compose

    Adding this rule will trigger notifications when integration tests of a
    compose are running in the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith(
        'ci.pipeline.package.test.functional.running')


@hint(topics=[_('ci.pipeline.compose.test.integration.complete')], invertible=False)
def ci_compose_test_complete(config, message):
    """ Integration tests completed for a compose

    Adding this rule will trigger notifications when integration tests of a
    compose have completed in the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith(
        'ci.pipeline.package.test.functional.complete')


@hint(topics=[_('ci.pipeline.image.test.smoke.running')])
def ci_image_test_running(config, message):
    """ Smoke tests are running for an image

    Adding this rule will trigger notifications when smoke tests of an
    image are running in the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith(
        'ci.pipeline.image.test.smoke.running')


@hint(topics=[_('ci.pipeline.image.test.smoke.complete')])
def ci_image_test_complete(config, message):
    """ Smoke tests are running for an image

    Adding this rule will trigger notifications when smoke tests of an
    image have completed in the Fedora Atomic `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_.
    """
    return message['topic'].endswith(
        'ci.pipeline.image.test.smoke.complete')


# More interesting rules

@hint(topics=[_('ci.pipeline.image.test.smoke.complete')], invertible=False)
def ci_test_passed(config, message):
    """ Any of the tests run passed the CI pipeline

    Adding this rule will trigger notifications when any of the tests ran
    by the `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_ passed.
    """
    if not message['topic'].endswith(
            (
                'ci.pipeline.package.test.functional.complete',
                'ci.pipeline.compose.test.integration.complete',
                'ci.pipeline.image.test.smoke.complete',
                )
            ):
        return False

    return message.get('msg', {}).get('status', '').lower() == 'success'


@hint(topics=[_('ci.pipeline.image.test.smoke.complete')], invertible=False)
def ci_step_complete(config, message):
    """ Any steps of the CI pipeline completed successfully

    Adding this rule will trigger notifications when any of the steps of
    the `CI pipeline
    <https://fedoraproject.org/wiki/FedoraAtomicCI/pipeline>`_ completed.
    """
    return message['topic'].split('.')[3] == 'ci' \
        and message.get('msg', {}).get('status', '').lower() == 'success'
