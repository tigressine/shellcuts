#!/usr/bin/env python3
import shutil
import subprocess

# Remove shellcuts tree if it exists
try:
    shutil.rmtree('shellcuts')
except FileNotFoundError:
    pass

# Tree definition for deb builds
DEB_TREE = (('bin/', 'shellcuts/usr/bin', ()),
            ('pack/deb/', 'shellcuts/DEBIAN', ('build.py',)),
            ('docs/', 'shellcuts/usr/share/doc/shellcuts', ('shellcuts.1',)),
            ('docs/', 'shellcuts/usr/share/man/man1', ('*.txt','*.rst')),
            ('share/', 'shellcuts/usr/share/shellcuts', ()))

# Create shellcuts tree based on tree definition
for branch in DEB_TREE:
    shutil.copytree(branch[0],
                    branch[1],
                    ignore=shutil.ignore_patterns(*branch[2]))

# Make deb package
subprocess.run(('dpkg', '--build', 'shellcuts'))

# Remove shellcuts tree
shutil.rmtree('shellcuts')
