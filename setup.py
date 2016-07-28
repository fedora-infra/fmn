""" Setup file for fmn.sse """
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


def get_description():
    with open('README.md', 'r') as f:
        return ''.join(f.readlines()[2:])


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

requires = [
    'fedmsg',
    'pika',
    'twisted',
]

tests_require = [
    'mock',
    'pytest',
    'faker'  # for dev-data.py
]

setup(
    name='fmn.sse',
    version='0.1.0',
    description='Real time feed for fedmsg',
    long_description=get_description(),
    author='Szymon M',
    author_email='skrzepto@gmail.com',
    url="https://github.com/fedora-infra/fmn.sse/",
    # download_url="https://pypi.python.org/pypi/fmn.sse/",# not yet configured
    license='GPL',
    install_requires=requires,
    tests_require=tests_require,
    packages=['fmn.sse'],
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    cmdclass={'test': PyTest},
)
