""""""
import os
import shutil
from pathlib import Path
from .utils import error_message, load_version_info
from .constants import SHELLCUTS_FILE, SHELL_CONFIGS
from .database import DatabaseConnection

def command_bashmarks(enabled):
    """Enable or disable Bashmarks syntax.
    
    Determines which shells Shellcuts is configured to use, then either
    installs the bashmarks-alias files into the appropriate config folder, or
    removes them.
    """
    command = 'printf "{0} Bashmarks syntax.\n"'

    for install in [item for item in SHELLCUTS_FILE.parent.iterdir() if item.is_dir()]:
        if enabled is True:
            for f in SHELL_CONFIGS.joinpath(install.name).iterdir():
                if f.stem == 'bashmarks-aliases':
                    shutil.copyfile(f, install.joinpath(f.name))
                    break
            else:
                error_message("BadInstall")

        elif not enabled:
            for f in install.iterdir():
                if f.stem == 'bashmarks-aliases':
                    os.remove(f)
                    break

    print(command.format("Enabled" if enabled is True else "Disabled"))

def command_delete(shellcut):
    """Delete shellcut from database."""
    command = 'printf "Deleted shellcut \'{0}\'\n"'
    
    with DatabaseConnection(SHELLCUTS_FILE) as db:
        db.delete_shellcut(shellcut)

    print(command.format(shellcut))

def command_go(shellcut):
    """Access shellcut and return 'cd' command to shellcut dir."""
    command = 'cd "{0}"'

    with DatabaseConnection(SHELLCUTS_FILE) as db:
        path = db.get_shellcut_path(shellcut)

        if path is None:
            error_message("DoesNotExist")
        elif Path(path).exists():
            print(command.format(path))
        else:
            db.delete_shellcut(shellcut)
            error_message("BadPath")

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

    with DatabaseConnection(SHELLCUTS_FILE) as db:
        shellcuts = db.get_all_shellcuts()

    if shellcuts is not None and len(shellcuts) > 0:
        command += 'SHELLCUTS\n'
    
        for shellcut in shellcuts:
            command += '{0} : {1} : {2}\n'.format(*shellcut)
    else:
        command += '(No shellcuts yet. Create some with the -n flag!)\n'

    command += '"'
    print(command)

def command_move(shellcut):
    """Reinsert existing shellcut at new location."""
    command = 'printf "Moved shellcut \'{0}\'\n"'
    
    with DatabaseConnection(SHELLCUTS_FILE) as db:
        # The insert_shellcut function will delete old versions of the shellcut
        # and use the most recent version.
        db.insert_shellcut(shellcut, os.getcwd())

    print(command.format(shellcut))

def command_new(shellcut):
    """Add shellcut to database and print confirmation."""
    command = 'printf "Added new shellcut \'{0}\'\n"'
    
    with DatabaseConnection(SHELLCUTS_FILE) as db:
        db.insert_shellcut(shellcut, os.getcwd())

    print(command.format(shellcut))

def command_print(shellcut):
    """Print specific shellcut."""
    command = 'printf "{0} : {1} : {2}\n"'
    
    with DatabaseConnection(SHELLCUTS_FILE) as db:
        shellcut_tuple = db.get_shellcut(shellcut)
   
    if shellcut_tuple is not None:
        print(command.format(*shellcut_tuple))
    else:
        error_message("DoesNotExist")
   
def command_version(*_):
    """Echo version information found in F_VERSION."""
    lines = load_version_info()

    if lines is None:
        error_message("NoVersion")
    else:
        command = 'printf "'
        
        for line in lines:
            command += line
        command += '"'
        
        print(command)
