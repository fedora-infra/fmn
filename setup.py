""" Setup file for fmn.consumer """

import sys
import os
import logging

from setuptools import setup

# Ridiculous as it may seem, we need to import multiprocessing and logging here
# in order to get tests to pass smoothly on python 2.7.
try:
    import multiprocessing
    import logging
except:
    pass


def get_description():
    with open('README.rst', 'r') as f:
        return ''.join(f.readlines()[2:])

requires = [
    'fmn.lib',
    'fedmsg',
    'requests',
    'arrow',
    'bleach',
]

tests_require = [
    'nose',
]

setup(
    name='fmn.consumer',
    version='0.6.3',
    description='Backend worker daemon for Fedora Notifications',
    long_description=get_description(),
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url="https://github.com/fedora-infra/fmn.consumer/",
    download_url="https://pypi.python.org/pypi/fmn.consumer/",
    license='LGPLv2+',
    install_requires=requires,
    tests_require=tests_require,
    test_suite='nose.collector',
    packages=['fmn', 'fmn.consumer', 'fmn.consumer.backends'],
    namespace_packages=['fmn'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    entry_points={
        'moksha.consumer': [
            "fedmsg_notifications_consumer = fmn.consumer:FMNConsumer",
        ],
        'moksha.producer': [
            "fmn_confirmations_producer = fmn.consumer:ConfirmationProducer",
            "fmn_digest_producer = fmn.consumer:DigestProducer",
        ],
    },
)
