""" Setup file for fmn.web """

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
        return '\n'.join(f.readlines()[2:])

requires = [
    'SQLAlchemy>=0.8',
    'fmn.lib',
    'python-openid',
    'python-openid-cla',
    'python-openid-teams',
    'Flask<0.10',  # Because of that openid json bug.
    'Flask-openid',
    'wtforms',
    'docutils',
    'markupsafe',
    'pylibravatar',
    'pydns',
    'urllib3',
    'datanommer.models',
    'arrow',
]

tests_require = [
    'nose',
]

setup(
    name='fmn.web',
    version='0.2.6',
    description='Frontend Web Application for Fedora Notifications',
    long_description=get_description(),
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url="https://github.com/fedora-infra/fmn.web/",
    download_url="https://pypi.python.org/pypi/fmn.web/",
    license='LGPLv2+',
    install_requires=requires,
    tests_require=tests_require,
    test_suite='nose.collector',
    packages=['fmn', 'fmn.web'],
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
