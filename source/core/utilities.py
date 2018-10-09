"""A collection of utilities and constants necessary for Shellcuts.

Part of Shellcuts by Tiger Sachse.
"""
from pathlib import Path

# Constants for the whole program.
SHELL_DIRS = Path('~/.shellcuts/shells').expanduser()
VERSION_FILE = Path('~/.shellcuts/docs/VERSION.txt').expanduser()
MANUAL_FILE = Path('~/.shellcuts/docs/SHELLCUTS.man').expanduser()
SHELLCUTS_FILE = Path('~/.shellcuts/data/shellcuts.json').expanduser()
ERRORS = {
    'DoesNotExist' : 'That shellcut does not exist.',
    'NoVersion'    : 'Version information not found.',
    'BadPath'      : 'The path associated with this shellcut is invalid.',
}

def throw_error(error):
    """Print an error message."""
    command = 'printf "ERROR {0}: {1}\n"'
    print(command.format(error, ERRORS[error]))
    exit(0)


def throw_help():
    """Print a help message."""
    script = (
        'Shellcuts usage: \$ sc [-f] <shellcut>',
        '---------------------------------------------------',
        'Create a new shellcut for the current directory:',
        '    \$ sc -n example',
        '',
        'Jump to the example location:',
        '    \$ sc example',
        '',
        'Remove the example shellcut:',
        '    \$ sc -d example',
        '',
        'List all available shellcuts:',
        '    \$ sc -l',
        '',
        'See the manpage for more information and examples:',
        '    \$ sc --man'
    )
    command = 'printf "'
    
    for line in script:
        command += line + '\n'
    print(command + '"')
    exit(0)
