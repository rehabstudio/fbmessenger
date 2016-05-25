from codecs import open
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

long_description = ''

try:
    import subprocess
    import pandoc

    process = subprocess.Popen(
        ['which pandoc'],
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    pandoc_path = process.communicate()[0]
    pandoc_path = pandoc_path.strip('\n')

    pandoc.core.PANDOC_PATH = pandoc_path

    doc = pandoc.Document()
    doc.markdown = open('README.md').read()

    long_description = doc.rst
except:
    pass

test_requirements = [
    'pytest',
    'coverage',
    'pytest-cov',
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
    description='A python library to communicate with the Facebook Messenger API\'s',
    long_description=long_description,
    url='https://github.com/rehabstudio/fbmessenger',
    author='Ricky Dunlop',
    author_email='ricky@rehabstudio.com',
    license='Apache',
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
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
    keywords='Facebook Messenger',
)
