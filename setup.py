"""Setup file for fmn"""

import sys

from setuptools import setup, find_packages


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
    version='1.3.1',
    description='Library for fedmsg Notifications',
    long_description=get_description(),
    author='Fedora Infrastructure Team',
    author_email='infrastructure@lists.fedoraproject.org',
    url="https://github.com/fedora-infra/fmn",
    download_url="https://pypi.python.org/pypi/fmn/",
    license='LGPLv2+ and BSD',
    install_requires=requires,
    tests_require=get_requirements('dev-requirements.txt'),
    test_suite='fmn.tests',
    packages=find_packages(exclude=('fmn.tests', 'fmn.tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Framework :: Twisted',
    ],
    entry_points={
        'moksha.consumer': [
            "fedmsg_notifications_consumer = fmn.consumer:FMNConsumer",
        ],
        'console_scripts': [
            'fmn-createdb = fmn.lib.db:main',
        ],
    },
)
