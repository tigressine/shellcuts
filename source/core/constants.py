from pathlib import Path

ERRORS = {
    "DoesNotExist"  : "That shellcut does not exist.",
    "Unimplemented" : "This feature is unimplemented.",
    "NoVersion"     : "Version information not found.",
    "BadInstall"    : "Installed files are not in the expected place.",
    "BadPath"       : "The path associated with this shellcut is invalid."}
VERSION_FILE = Path('/usr/share/doc/shellcuts/META.txt')
SHELLCUTS_FILE = Path('~/.config/shellcuts/shellcuts.db').expanduser()
SHELL_CONFIGS = Path('/usr/share/shellcuts/')
