"""
"""
import compileall
from sys import argv as args
from pathlib import Path

paths = {
    'bin' : Path('/usr/bin'),
    'share' : Path('/usr/share'),
    'trigger' : Path('/home/tgsachse/Dropbox/Code/Shellcuts/junk')
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

def install_global():
    """
    """
    pass

def install_local():
    """
    """
    

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
