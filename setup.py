""" Setup file for fmn.sse """
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


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


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='fmn.sse',
    version='0.1.1',
    description='Real time feed for fedmsg',
    long_description=get_description(),
    author='Szymon M',
    author_email='skrzepto@gmail.com',
    url="https://github.com/fedora-infra/fmn.sse/",
    # download_url="https://pypi.python.org/pypi/fmn.sse/",# not yet configured
    license='GPL',
    install_requires=get_requirements('requirements.txt'),
    tests_require=get_requirements('tests-requirements.txt'),
    packages=['fmn', 'fmn.sse'],
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass={'test': PyTest},
)
