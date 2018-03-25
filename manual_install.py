"""
"""
from sys import argv as args

def check_if_local_install():
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

def install_global():
    pass

def install_local():
    pass

def main():
    local = check_if_local_install()
