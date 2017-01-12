""" Setup file for fmn.sse """
from setuptools import setup


def get_description():
    with open('README.md', 'r') as f:
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
    name='fmn_sse',
    version='0.2.1',
    description='Real time feed for fedmsg',
    long_description=get_description(),
    author='Fedora Infrastructure Team and Szymon M',
    author_email='infrastructure@lists.fedoraproject.org',
    url="https://github.com/fedora-infra/fmn.sse/",
    download_url="https://pypi.python.org/pypi/fmn_sse/",
    license='GPLv2+',
    install_requires=get_requirements('requirements.txt'),
    tests_require=get_requirements('tests-requirements.txt'),
    test_suite='tests',
    packages=['fmn_sse'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
