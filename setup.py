#!/usr/bin/env python3
"""Builds shellcuts package.

This setup script builds the shellcuts package for distribution.

Arguments:
    See arguments for setup.py

Returns:
    None.

To Do:
    -Clean up error messaging of argparse
    -Add support for tab completion
    -Write readme
    -Get into ubuntu repos
    -Get working with all shells

Legal:
    Author: Tiger Sachse
    License: GPLv3
    Version: 1.1.0
    Initial Release: 12/31/2017
    Current Release: 01/02/2018
"""

from setuptools import setup

F_DESCRIPTION = 'docs/PYPI_DESCRIPTION.txt'

def load_long_description():
    """Load description for PyPI from file"""
    with open(F_DESCRIPTION, 'r') as f:
        long_description = f.read()

    return long_description

setup(
    name='shellcuts',
    version='1.1.0',
    author='Tiger Sachse',
    description='Shortcuts for your shell.',
    long_description=load_long_description(),
    url='https://www.github.com/tgsachse/shellcuts',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Unix Shell',
        'Topic :: System',
        'Topic :: Terminals',
        'Topic :: Utilities'],
    keywords='bookmark bashmark shell terminal cd chdir utility workflow',
    packages=['shellcuts'],
    python_requires='>=3',
    data_files=[
        ('bin', ['shellcuts/sc-handler',
                 'shellcuts/sc-init',
                 'shellcuts/shellcuts.sh'])]
)
