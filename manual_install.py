"""
"""
import compileall
from sys import argv as args
from pathlib import Path
import subprocess
from tarfile import TarFile

VERSION = 'v1.2.1'
paths = {
    'bin' : Path('/usr/bin'),
    'share' : Path('/usr/share'),
    #'trigger' : Path('/home/tgsachse/Dropbox/Code/Shellcuts/junk')
}

def check_local_install():
    """
    """
    if len(args) > 1:
        if args[1] == '--local':
            return True
        elif args[1] == '--global':
            return False
        else:
            print("Unknown arguments passed to script.")
            exit(0)
    else:
        return False

def check_paths():
    """
    """
    for key, path in paths.items():
        if not path.exists():
            return False
    else:
        return True

def check_package_managers():
    """
    """
    pass

def install_global():
    """
    """
    check_package_managers()

def install_local():
    """
    """
    D_SHELLCUTS = Path('~/.shellcuts').expanduser()
    D_SHELLCUTS.mkdir(parents=True, exist_ok=True)
    DEST = D_SHELLCUTS.joinpath('git_temp')
    command = ('wget', 
               'https://github.com/tgsachse/shellcuts/archive/{}.tar.gz'.format(VERSION),
               '-P',
               str(DEST))#check this isnt possible with a lib

    subprocess.run(command)
    DEST = DEST.joinpath('{}.tar.gz'.format(VERSION))
    TarFile(str(DEST)).extractall()

    LOCAL_TREE = (
        ('bin', 'bin/'),
        ('share', 'share/'),
        ('docs', 'docs/'),
        ('man', 'man/man1')
    )

    

    # make sure weve got this bitch downloaded
    # compile the binaries
    # move bytecode to bin
    # move share tree to share
    # move docs to docs
    # mkdir for man and move man to man
    ####### add to bash plugin and rest to update bin path
    # destroy git


def main():
    """
    """
    if check_local_install():
        install_local()
    elif check_paths():
        install_global()
    else:
        print("Filesystem unsupported. Try installing locally.")

main()
