from pathlib import Path

SHELL_DIRS = Path('~/.shellcuts/shells').expanduser()
VERSION_FILE = Path('~/.shellcuts/docs/VERSION.txt').expanduser()
SHELLCUTS_FILE = Path('~/.shellcuts/data/shellcuts.json').expanduser()
ERRORS = {
    'DoesNotExist'  : 'That shellcut does not exist.',
    'Unimplemented' : 'This feature is unimplemented.',
    'NoVersion'     : 'Version information not found.',
    'BadInstall'    : 'Installed files are not in the expected place.',
    'BadPath'       : 'The path associated with this shellcut is invalid.',
}
