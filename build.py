#!/usr/bin/env python3
"""Builds Shellcuts into a variety of packages.

Feel free to submit additions to this script to include more types of packages.
One of my primary goals for Shellcuts is universal support.

Part of Shellcuts by Tgsachse.
"""
import os
import shutil
import subprocess
from pathlib import Path
from sys import argv as args

def chop_trees(trees):
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
    chop_trees((BUILD))

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
    chop_trees((BUILD))

def build_rpm():
    """Build RPM package from source."""
    ARCHIVE = Path('v1.2.0')
    SOURCE_SPEC = 'pack/rpm/shellcuts.spec'
    RPM_BUILD = Path('~/rpmbuild').expanduser()
    TARBALL_CONTENTS = ('docs', 'share', 'bin')
    DESTINATION_SPEC = RPM_BUILD.joinpath('SPECS/shellcuts.spec')
    TARBALL = RPM_BUILD.joinpath(Path('SOURCES/').joinpath(ARCHIVE))

    # Cuts down leftover trees.
    chop_trees((ARCHIVE, RPM_BUILD))

    # Copies source into tarball folder.
    for directory in TARBALL_CONTENTS:
        shutil.copytree(directory, ARCHIVE.joinpath(directory))

    # Generates the RPM build folder.
    subprocess.run('rpmdev-setuptree')
     
    # Compresses a tarball from source and copy files into RPM build folder.
    shutil.make_archive(TARBALL, 'gztar', os.getcwd(), ARCHIVE)
    shutil.copy(SOURCE_SPEC, DESTINATION_SPEC)
    
    # Builds the RPM using the SPEC file.
    subprocess.run(('rpmbuild', '-bb', DESTINATION_SPEC))
   
    # Makes the DIST directory if it doesn't exist.
    DIST.mkdir(exist_ok=True)

    # Moves the RPM back to the project directory.
    for package in RPM_BUILD.joinpath('RPMS/noarch/').iterdir():
        shutil.copy(package, DIST)

    # Chops down all generated trees.
    chop_trees((RPM_BUILD, ARCHIVE))


### MAIN PROGRAM ###
DIST = Path.cwd().joinpath('dist/')

if len(args) > 1:
    if args[1] == 'deb':
        build_deb()
        quit()
    elif args[1] == 'rpm':
        build_rpm()
        quit()

print("Pass either 'deb' or 'rpm' as the first argument.")
