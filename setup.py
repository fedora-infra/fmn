""" Setup file for fmn.consumer """

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


setup(
    name='fmn.consumer',
    version='1.0.3',
    description='Backend worker daemon for Fedora Notifications',
    long_description=get_description(),
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url="https://github.com/fedora-infra/fmn.consumer/",
    download_url="https://pypi.python.org/pypi/fmn.consumer/",
    license='LGPLv2+',
    install_requires=get_requirements(),
    tests_require=get_requirements('tests-requirements.txt'),
    test_suite='tests',
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
    },
)
