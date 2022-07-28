import io
import os
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

long_description = ''
short_description='A python library to communicate with the Facebook Messenger API\'s'


try:
    with io.open('README.md', encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = short_description


test_requirements = [
    'pytest',
    'coverage',
    'pytest-cov',
    'pytest-catchlog',
    'responses'
]

# Get the version
version_regex = r'__version__ = ["\']([^"\']*)["\']'
with open('fbmessenger/__init__.py', 'r') as f:
    text = f.read()
    match = re.search(version_regex, text)

    if match:
        VERSION = match.group(1)
    else:
        raise RuntimeError("No version number found!")


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='fbmessenger',
    version=VERSION,
    description=short_description,
    long_description=long_description,
    url='https://github.com/rehabstudio/fbmessenger',
    author='Ricky Dunlop',
    author_email='hello@rickydunlop.co.uk',
    license='Apache',
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=['requests>=2.0'],
    packages=['fbmessenger'],
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
    keywords='Facebook Messenger Bot Chatbot',
)
