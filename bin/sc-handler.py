"""Handles arguments from main shell function.

This is the core engine of the program. It handles all relevant options and
commands. After the arguments are parsed and handled, a command is returned to
the calling shell function.

Part of Shellcuts by Tgsachse.
"""
import os
import json
import shutil
import argparse
from pathlib import Path

### CONSTANTS ###
# Can be changed to save the shellcuts in a different location.
F_SHELLCUTS_JSON = Path('~/.config/shellcuts/shellcuts.json').expanduser()
D_SHELL_CONFIGS = Path('/usr/share/shellcuts/')
F_VERSION = '/usr/share/doc/shellcuts/META.txt'


### SUBCLASSES ###
class Parser(argparse.ArgumentParser):
    """Subclass of ArgumentParser.

    Necessary to override error method in ArgumentParser. Sometimes the
    ArgumentParser throws errors (if argument syntax is bad, for example) and
    in all of these cases I want the help menu to appear, instead of the
    provided error messages.
    """
    def error(*_):
        """Call help command in case of error."""
        command_help()
        exit(0)


### COMMANDS ###
def command_bashmarks(enable):
    """Enable or disable Bashmarks syntax.
    
    Determines which shells Shellcuts is configured to use, then either
    installs the bashmarks-alias files into the appropriate config folder, or
    removes them.
    """
    command = 'printf ""'

    for install in [item for item in F_SHELLCUTS_JSON.parent.iterdir() if item.is_dir()]:
        if enable:
            for f in D_SHELL_CONFIGS.joinpath(install.name).iterdir():
                if f.stem == 'bashmarks-aliases':
                    shutil.copyfile(f, install.joinpath(f.name))
                    break
            else:
                error_message(4)

        elif not enable:
            for f in install.iterdir():
                if f.stem == 'bashmarks-aliases':
                    os.remove(f)
                    break

    print(command)

def command_delete(shellcut):
    """Delete shellcut and write to file."""
    command = 'printf ""'
    
    shellcuts.pop(shellcut, None)
    write_shellcuts()
    
    print(command)

def command_go(shellcut):
    """Access shellcut and return 'cd' command to shellcut dir."""
    try:
        command = 'cd "' + shellcuts[shellcut] + '"'
        if Path(shellcuts[shellcut]).exists():
            print(command)
        else:
            error_message(5)
    except KeyError:
        error_message(1)

def command_help(*_):
    """Print a small help menu to the screen."""
    HELP_SCRIPT = (
        'Shellcuts usage: \$ sc [--flag] <shellcut>',
        '----------------------------------------------------------------',
        'Create a new shellcut for the current directory (named example):',
        '    \$ sc -n example',
        '',
        'Jump to that location from anywhere else on the system:',
        '    \$ sc example',
        '',
        'Remove that shellcut:',
        '    \$ sc -d example',
        '',
        'List all available shellcuts:',
        '    \$ sc -l',
        '',
        'See the manpage for lots more information and examples:',
        '    \$ man shellcuts')
    command = 'printf "'
    
    for line in HELP_SCRIPT:
        command += line + '\n'
    command += '"'

    print(command)

def command_init(*_):
    """Run initialization script."""
    command = 'python3 /usr/bin/sc-init'
    
    print(command)

def command_list(*_):
    """List all shellcuts."""
    command = 'printf "'
    
    if len(shellcuts) > 0:
        command += 'SHELLCUTS\n'
    
        for shellcut in shellcuts:
            command += '{0} : {1}\n'.format(shellcut, shellcuts[shellcut])
    else:
        command += '(No shellcuts yet. Create some with the -n flag!)\n'

    command += '"'
    print(command)

def command_new(shellcut):
    """Add shellcut and write to file."""
    command = 'printf ""'
    
    shellcuts[shellcut] = os.getcwd()
    write_shellcuts()
    
    print(command)

def command_print(shellcut):
    """Print specific shellcut."""
    try:
        command = 'printf "' + shellcut + ' : ' + shellcuts[shellcut] + '\n"'
        print(command)
    except KeyError:
        error_message(1)

def command_version(*_):
    """Echo version information found in F_VERSION."""
    command = 'printf "'
    
    for line in load_version_info():
        command += line
    command += '"'
    
    print(command)

def command_z(enable):
    """Unimplemented."""
    error_message(2)


### HELPER FUNCTIONS ###
def create_parser():
    """Create an argparse parser.

    Defines arguments and then returns the parser.
    """
    parser = Parser(add_help=False)
    
    parser.add_argument('shellcut', nargs='?', default=None)
    parser.add_argument('-d', '--delete')
    parser.add_argument('-h', '--help', action='store_true', default=None)
    parser.add_argument('-l', '--list', action='store_true', default=None)
    parser.add_argument('-n', '--new')
    parser.add_argument('-p', '--print')
    parser.add_argument('--version', action='store_true', default=None)
    parser.add_argument('--init', action='store_true', default=None)
    parser.add_argument('--enable-bashmarks-syntax',
                        action='store_true',
                        dest='bashmarks',
                        default=None)
    parser.add_argument('--disable-bashmarks-syntax',
                        action='store_false',
                        dest='bashmarks',
                        default=None)
    parser.add_argument('--enable-z',
                        action='store_true',
                        dest='z',
                        default=None)
    parser.add_argument('--disable-z',
                        action='store_false',
                        dest='z',
                        default=None)

    return parser

def error_message(error):
    """Echo an error message.
    
    Includes a master dictionary of all supported errors. These are accessible
    by number.
    """
    ERRORS = {
        1 : "That shellcut does not exist.",
        2 : "This feature is unimplemented.",
        3 : "Version information not found.",
        4 : "Installed files are not in the expected place.",
        5 : "The path associated with this shellcut is invalid."}
    
    command = 'printf "ERROR {0}: {1}\n"'.format(error, ERRORS[error])
    
    print(command)

def load_shellcuts():
    """Load the shellcuts file.

    Returns empty dictionary if the file does not exist.
    """
    try:
        with open(F_SHELLCUTS_JSON, 'r') as f:
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
    F_SHELLCUTS_JSON.parent.mkdir(parents=True, exist_ok=True)

    with open(F_SHELLCUTS_JSON, 'w') as f:
        json.dump(shellcuts, f)


### START MAIN PROGRAM ###
parser = create_parser()
arguments, unknown = parser.parse_known_args()
shellcuts = load_shellcuts()

# If anything unknown is passed, show help and exit.
if len(unknown) > 0:
    command_help()
    exit(0)

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
        # Passes value to corresponding function. Functions are designed to
        # handle this value even if they don't need it.
        pair[1](pair[0])
        break
else:
    command_help()
