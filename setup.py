#!/usr/bin/env python3
"""Builds shellcuts package.

This setup script builds the shellcuts package for distribution.

Arguments:
    See arguments for setup.py

Returns:
    None.

Legal:
    Author: Tiger Sachse
    License: GPLv3
    Version: 1.1.1
    Initial Release: 12/31/2017
    Current Release: 01/08/2018
"""
LONG_DESCRIPTION = 'Please see the GitHub project page for more ' +
                   'information, located at https://www.github.com/tgsachse/shellcuts'

from setuptools import setup

setup(
    name='shellcuts',
    version='1.1.1',
    author='Tiger Sachse',
    description='Directory shortcuts for your shell.',
    long_description=LONG_DESCRIPTION
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
                 'shellcuts/shellcuts.sh']),
        ('share/doc/shellcuts', ['docs/CHANGES.txt',
                                 'docs/LICENSE.txt',
                                 'docs/README.rst']),
        ('share/man/man1',['docs/shellcuts.1'])]
)
