#!/usr/bin/env python3
from setuptools import setup

# TODO
# clean up error messaging of argparse
# Add support for tab completion
# Write readme
# Add comments
# Get into ubuntu repos?
# Get working with all shells


def get_version():
    return '1.0.2'

def get_long_description():
    return 'Shortcuts for your shell.'

setup(
    name='shellcuts',
    version=get_version(),
    author='Tiger Sachse',
    description='Shortcuts for your shell.',
    long_description=get_long_description(),
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
