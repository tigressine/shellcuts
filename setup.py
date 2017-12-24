#! /usr/bin/env python3
from setuptools import setup

# TODO
# Add -v version
# Support original bashmarks commands
# Add support for tab completion
# Write readme
# Comments
# Move arg handling around
# Get into ubuntu repos?
# Get working with zsh

def get_version():
    return '1.0.1'

def get_long_description():
    return 'Bookmarks for your shell.'

setup(
    name='bashmarks',
    version=get_version(),
    author='Tiger Sachse',
    description='Bookmarks for your shell.',
    long_description=get_long_description(),
    url='https://www.github.com/tgsachse/bashmarks',
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
    packages=['bashmarks'],
    python_requires='>=3',
    data_files=[
        ('bin', ['bashmarks/bm-handler',
                 'bashmarks/bm-init',
                 'bashmarks/bash_marks'])]
)
