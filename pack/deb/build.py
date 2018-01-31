#! /usr/bin/env python3
import subprocess
import pathlib
import shutil

tree = (('bin/*', 'shellcuts/bin', ()),
        ('pack/deb/*', 'shellcuts/DEBIAN', ('pack/deb/build.py')),
        ('docs/*', 'shellcuts/usr/share/doc/shellcuts', ('docs/shellcuts.1')),
        ('docs/shellcuts.1', 'shellcuts/usr/share/man/man1', ()),
        ('share/*', 'shellcuts/usr/share/shellcuts', ()))

for branch in tree:
    shutil.copytree(branch[0], branch[1], ignore=branch[2])
