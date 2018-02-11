"""Handles arguments from main shell function.

This is the core engine of the program. It handles all relevant options and
commands. After the arguments are parsed and handled, a command is returned to
the calling shell function.

Part of Shellcuts by Tgsachse.
"""
import os
import json
import pathlib
import argparse

### CONSTANTS ###
# Can be changed to save the shellcuts in a different location.
D_SHELLCUTS = os.path.expanduser('~/.config/shellcuts/')
F_SHELLCUTS = 'shellcuts.json'
F_VERSION = '/usr/share/doc/shellcuts/META.txt'


### COMMANDS ###
def command_bashmarks():
    """Unimplemented."""
    error_message(2)

def command_delete():
    """Delete shellcut and write to file."""
    command = ':'
    shellcuts.pop(arguments.delete, None)
    write_shellcuts()
    print(command)

def command_go():
    """Access shellcut and return 'cd' command to shellcut dir."""
    try:
        command = 'cd ' + shellcuts[arguments.shellcut]
        print(command)
    except KeyError:
        error_message(1)

def command_help():
    """Open man page."""
    command = 'man shellcuts'
    print(command)

def command_init():
    """Run initialization script."""
    command = '/usr/bin/sc'
    print(command)

def command_list():
    """List all shellcuts."""
    command = 'printf "SHELLCUTS\n'
    for shellcut in shellcuts:
        command += '{0} : {1}\n'.format(shellcut, shellcuts[shellcut])
    command = command[:-1] + '\n"'
    print(command)

def command_new():
    """Add shellcut and write to file."""
    command = ':'
    shellcuts[arguments.new] = os.getcwd()
    write_shellcuts()
    print(command)

def command_print():
    """Print specific shellcut."""
    try:
        command = 'printf "' + arguments.print + ' : ' + shellcuts[arguments.print] + '\n"'
        print(command)
    except KeyError:
        error_message(1)

def command_version():
    """Echo version information found in F_VERSION."""
    command = 'printf "'
    for line in load_version_info():
        command += line
    command = command[:-1] + '\n"'
    print(command)

def command_z():
    """Unimplemented."""
    error_message(2)


### HELPER FUNCTIONS ###
def create_parser():
    """Create an argparse parser.

    Defines arguments and then returns the parser.
    """
    parser = argparse.ArgumentParser(add_help=False)
    
    parser.add_argument('shellcut', default=None, nargs='?')
    parser.add_argument('-d', '--delete')
    parser.add_argument('-h', '--help', action='store_true', default=None)
    parser.add_argument('-l', '--list', action='store_true', default=None)
    parser.add_argument('-n', '--new')
    parser.add_argument('-p', '--print')
    parser.add_argument('--version', action='store_true', default=None)
    parser.add_argument('--init', action='store_true', default=None)
    parser.add_argument('--enable-bashmarks-syntax',
                        action='store_true',
                        default=None,
                        dest='bashmarks')
    parser.add_argument('--disable-bashmarks-syntax',
                        action='store_false',
                        default=None,
                        dest='bashmarks')
    parser.add_argument('--enable-z',
                        action='store_true',
                        default=None,
                        dest='z')
    parser.add_argument('--disable-z',
                        action='store_false',
                        default=None,
                        dest='z')

    return parser

def error_message(error):
    """Echo an error message.
    
    Includes a master dictionary of all supported errors. These are accessible
    by number.
    """
    ERRORS = {1 : "That shellcut does not exist",
              2 : "This feature is unimplemented.",
              3 : "Version information not found."}
    command = 'printf "ERROR {0}: {1}"'.format(error, ERRORS[error])
    print(command)

def load_shellcuts():
    """Load the shellcuts file.

    Returns empty dictionary if the file does not exist.
    """
    try:
        with open(D_SHELLCUTS + F_SHELLCUTS, 'r') as f:
            shellcuts = json.load(f)
    except FileNotFoundError:
        shellcuts = {}

    return shellcuts

def load_version_info():
    """Load version information found at F_VERSION."""
    try:
        with open(F_VERSION, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        error_message(3)
        exit(0)

def write_shellcuts():
    """Write shellcuts to file.
    
    Creates appropriate directory if it doesn't exist.
    """
    if not pathlib.Path(D_SHELLCUTS).is_dir():
        pathlib.Path(D_SHELLCUTS).mkdir(parents=True)

    with open(D_SHELLCUTS + F_SHELLCUTS, 'w') as f:
        json.dump(shellcuts, f)


### START MAIN PROGRAM ###
parser = create_parser()
arguments = parser.parse_args()
shellcuts = load_shellcuts()

# This tuple associates arguments from the parser with their functions.
command_pairs = (
    (arguments.help, command_help),
    (arguments.list, command_list),
    (arguments.version, command_version),
    (arguments.init, command_init),
    (arguments.bashmarks, command_bashmarks),
    (arguments.z, command_z),
    (arguments.delete, command_delete),
    (arguments.new, command_new),
    (arguments.print, command_print),
    (arguments.shellcut, command_go))

# For each in tuple, if value is not 'None', execute associated function.
for pair in command_pairs:
    if pair[0] != None:
        pair[1]()
        exit(0)

command_help()
