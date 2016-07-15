""" Setup file for fmn.rules """

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
    'python-fedora',
    'fedmsg',
    'fedmsg_meta_fedora_infrastructure',
    'dogpile.cache',
    'six',
]

tests_require = [
    'nose',
]

setup(
    name='fmn.rules',
    version='0.9.0',
    description='Message processing rules for Fedora Notifications',
    long_description=get_description(),
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url="https://github.com/fedora-infra/fmn.rules",
    download_url="https://pypi.python.org/pypi/fmn.rules/",
    license='LGPLv2+',
    install_requires=requires,
    tests_require=tests_require,
    test_suite='nose.collector',
    packages=['fmn', 'fmn.rules'],
    namespace_packages=['fmn'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
