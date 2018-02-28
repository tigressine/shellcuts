#!/usr/bin/env python3
"""Builds Shellcuts into a variety of packages.

Feel free to submit additions to this script to include more types of packages.
One of my primary goals for Shellcuts is universal support.

Part of Shellcuts by Tgsachse.
"""
import os
import shutil
import subprocess
from sys import argv as args
from os.path import expanduser

def kill_trees(trees):
    """Remove each directory tree in trees if it exists."""
    for tree in trees:
        try:
            shutil.rmtree(tree)
        except FileNotFoundError:
            pass

def build_deb():
    """Build deb package from source."""
    
    # Tree structure for deb package.
    BUILD = 'shellcuts'
    DEB_TREE = (
        ('bin/', 'shellcuts/usr/bin/', ()),
        ('pack/deb/', 'shellcuts/DEBIAN/', ()),
        ('docs/', 'shellcuts/usr/share/doc/shellcuts/', ('shellcuts.1',)),
        ('docs/', 'shellcuts/usr/share/man/man1/', ('*.txt','*.rst')),
        ('share/', 'shellcuts/usr/share/shellcuts/', ())
    )
    
    # Cut down leftover trees.
    #print("firstcut")
    kill_trees((BUILD))

    # Create shellcuts tree based on DEB_TREE tuple.
    for branch in DEB_TREE:
        shutil.copytree(branch[0],
                        branch[1],
                        ignore=shutil.ignore_patterns(*branch[2]))

    # Build deb package.
    subprocess.run(('dpkg', '--build', 'shellcuts'))
    #shutil.move('shellcuts.deb', DIST)
    
    # Chop down all new trees.
    #print("chopping")
    kill_trees((BUILD))

def build_rpm():
    """Build RPM package from source."""

    ARCHIVE = 'shellcuts-1.1.2'
    RPM_BUILD = expanduser('~/rpmbuild')
    TARBALL_CONTENTS = ['docs/', 'share/', 'bin/']
    TARBALL = expanduser('~/rpmbuild/SOURCES/') + ARCHIVE

    # Cut down leftover trees.
    kill_trees((ARCHIVE, DIST, RPM_BUILD))

    # Copy source into tarball folder
    for directory in TARBALL_CONTENTS:
        shutil.copytree(directory, '{}/{}'.format(ARCHIVE, directory))

    # Generate the RPM build folder
    subprocess.run('rpmdev-setuptree')
    
    # Compress a tarball from source and copy files into RPM build folder
    shutil.make_archive(TARBALL, 'gztar', os.getcwd(), ARCHIVE)
    shutil.copy2('pack/rpm/shellcuts.spec', RPM_BUILD + '/SPECS/')

    # Build the RPM using the SPEC file
    subprocess.run(('rpmbuild', '-bb', RPM_BUILD + '/SPECS/shellcuts.spec'))
    
    # Move the RPM back to the project directory
    shutil.move(RPM_BUILD + '/RPMS/noarch/', DIST)

    # Chop down all generated trees
    kill_trees((RPM_BUILD, ARCHIVE))


### MAIN PROGRAM ###
DIST = os.getcwd() + '/dist'

if len(args) > 1:
    if args[1] == 'deb':
        build_deb()
        quit()
    elif args[1] == 'rpm':
        build_rpm()
        quit()

print("Pass either 'deb' or 'rpm' as the first argument.")
