"""Setup file for fmn"""

import sys

from setuptools import setup


def get_description():
    with open('README.rst', 'r') as f:
        return ''.join(f.readlines()[2:])


def get_requirements(filename='requirements.txt'):
    """
    Get the contents of a file listing the requirements.

    :param filename: path to a requirements file
    :type  filename: str

    :returns: the list of requirements
    :return type: list
    """
    with open(filename) as f:
        return [
            line.rstrip().split('#')[0]
            for line in f.readlines()
            if not line.startswith('#')
        ]


requires = get_requirements()
if sys.version_info[0] == 2 and sys.version_info[1] <= 6:
    requires.append("ordereddict")


setup(
    name='fmn',
    version='1.0.0',
    description='Library for Fedora Notifications',
    long_description=get_description(),
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url="https://github.com/fedora-infra/fmn",
    download_url="https://pypi.python.org/pypi/fmn/",
    license='LGPLv2+',
    install_requires=requires,
    tests_require=get_requirements('tests-requirements.txt'),
    test_suite='tests',
    packages=['fmn', 'fmn.rules', 'fmn.lib', 'fmn.consumer', 'fmn.consumer.backends'],
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
    },
)
