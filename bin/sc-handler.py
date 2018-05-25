"""Handles arguments from main shell function.

This is the core engine of the program. It handles all relevant options and
commands. After the arguments are parsed and handled, a command is returned to
the calling shell function.

Part of Shellcuts by Tgsachse.
"""
import os
import json ##
import shutil
import sqlite3
import argparse
from pathlib import Path ####

### CONSTANTS ###
# Can be changed to save the shellcuts in a different location.
F_SHELLCUTS_JSON = Path('~/.config/shellcuts/shellcuts.json').expanduser()    ####
D_SHELL_CONFIGS = Path('/usr/share/shellcuts/')
F_VERSION = '/usr/share/doc/shellcuts/META.txt'
F_SHELLCUTS = Path('~/.config/shellcuts/shellcuts.db').expanduser()

### SUBCLASSES ###
class DatabaseConnection:
    """An SQLite database connection containing shellcuts."""
    def __init__(self, path):
        """Save path of database as self.path."""
        self.path = path

    def __enter__(self):
        """Initialize connection and cursor."""
        if Path(self.path).is_file():
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
        else:
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
            self.create()

        return self

    def __exit__(self, type, value, traceback):
        """Save changes to database and close connection."""
        self.connection.commit()
        self.connection.close()

    def flush(self):
        """Delete all data from database."""
        self.cursor.execute('DELETE FROM table_shellcuts')
        self.cursor.execute('DELETE FROM table_defaults')
        
    def create(self):
        """Create neccessary tables in database."""
        self.cursor.execute("""CREATE TABLE table_shellcuts (name TEXT,
                                                             path TEXT,
                                                             command TEXT)""")
        self.cursor.execute("""CREATE TABLE table_defaults (enabled BOOLEAN,
                                                            command TEXT)""")
        self.set_default_command(False)

    def get_default_command(self):
        """Get the default command from table_defaults."""
        self.cursor.execute('SELECT command FROM table_defaults')

        command = self.cursor.fetchone()

        return None if command is None else command[0]

    def set_default_command(self, enabled, command=None):
        """Toggle default flag in table_defaults and set command if true."""
        self.cursor.execute('SELECT * FROM table_defaults')
       
        # If the table_defaults is empty, add a new entry.
        if self.cursor.fetchone() is None:
            self.cursor.execute('INSERT INTO table_defaults VALUES (?,?)',
                                (enabled, command))
        # Else if flag is being set to true, set both flag and command.
        elif enabled is True:
            self.cursor.execute('UPDATE table_defaults SET enabled=?, command=?',
                                (enabled, command))
        # Else flag is being set to false. Ignores command.
        else:
            self.cursor.execute('UPDATE table_defaults SET enabled=?',
                                (enabled,))

    def insert_shellcut(self, name, path):
        """Insert shellcut into database."""

        # If the shellcut already exists in the table, delete it first.
        if self.get_shellcut(name) is not None:
            self.delete_shellcut(name)

        self.cursor.execute('INSERT INTO table_shellcuts VALUES (?,?,?)',
                            (name, path, None))

    def delete_shellcut(self, name):
        """Delete a shellcut from the database."""
        self.cursor.execute('DELETE FROM table_shellcuts WHERE name=?', (name,))

    def get_shellcut(self, name):
        """Get path, name, and command of named shellcut."""
        self.cursor.execute('SELECT * FROM table_shellcuts WHERE name=?',
                            (name,))

        return self.cursor.fetchone()

    def get_all_shellcuts(self):
        """Get all shellcuts in database."""
        self.cursor.execute('SELECT * FROM table_shellcuts')

        return self.cursor.fetchall()

    def get_shellcut_path(self, name):
        """Get path of named shellcut."""
        shellcut = self.get_shellcut(name)
        
        return None if shellcut is None else shellcut[1]

    def get_shellcut_command(self, name):
        """Get follow command for shellcut."""
        shellcut = self.get_shellcut(name)

        # If the fetch fails, returns None.
        if shellcut is None:
            return None
        # If the command is None and default commands are enabled, returns
        # the default command.
        elif shellcut[2] is None and self.check_default_command_enabled():
            return self.get_default_command()
        # Else returns the custom command.
        else:
            return shellcut[2]

    def set_shellcut_command(self, name, command):
        """Set follow command for shellcut."""
        self.cursor.execute('UPDATE table_shellcuts SET command=? WHERE name=?',
                            (command, name))
    
    def check_default_command_enabled(self):
        """Check if default commands are enabled."""
        self.cursor.execute('SELECT enabled FROM table_defaults')

        enabled = self.cursor.fetchone()

        return None if enabled is None else enabled[0]

class Parser(argparse.ArgumentParser):
    """Subclass of ArgumentParser.

    Necessary to override error method in ArgumentParser. Sometimes the
    ArgumentParser throws errors (if argument syntax is bad, for example) and
    in all of these cases I want the help menu to appear, instead of the
    provided error messages. This subclass also provides the ability to create
    a base argument to attempt before parsing the rest, improving speed when
    jumping.
    """
    def __init__(self, *args, **kwargs): #### add no help menu here so it doesnt have to be passed
        """Initialize by initializing super and adding base argument."""
        super().__init__(*args, **kwargs)

        self.add_argument('shellcut', nargs='?', default=None)

    def add_additional_arguments(self):
        """Add flags to parser."""
        self.add_argument('-d', '--delete')
        self.add_argument('-h', '--help', action='store_true', default=None)
        self.add_argument('-l', '--list', action='store_true', default=None)
        self.add_argument('-n', '--new')
        self.add_argument('-p', '--print')
        self.add_argument('--version', action='store_true', default=None)
        self.add_argument('--init', action='store_true', default=None)
        self.add_argument('--enable-bashmarks-syntax',
                          action='store_true',
                          dest='bashmarks',
                          default=None)
        self.add_argument('--disable-bashmarks-syntax',
                          action='store_false',
                          dest='bashmarks',
                          default=None)
        self.add_argument('--enable-z',
                          action='store_true',
                          dest='z',
                          default=None)
        self.add_argument('--disable-z',
                          action='store_false',
                          dest='z',
                          default=None)
    
    def error(self, message):
        """Call help command in case of error."""
        command_help()
        exit(0)


### COMMANDS ###
def command_bashmarks(enable): ######### maybe dunno
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

def command_delete(shellcut): #################
    """Delete shellcut and write to file."""
    command = 'printf ""'
    
    shellcuts.pop(shellcut, None)
    write_shellcuts()
    
    print(command)

def command_go(shellcut): #######################33
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

def command_list(*_): #########
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

def command_move(shellcut):
    """Reinsert existing shellcut at new location."""
    command = 'printf "Moved shellcut\'{0}\'"'.format(shellcut)
    
    with DatabaseConnection(F_SHELLCUTS) as db:
        # The insert_shellcut function will delete old versions of the shellcut
        # and use the most recent version.
        db.insert_shellcut(shellcut, os.getcwd())

    print(command)

def command_new(shellcut):
    """Add shellcut to database and print confirmation."""
    command = 'printf "Added new shellcut\'{0}\'"'.format(shellcut)
    
    with DatabaseConnection(F_SHELLCUTS) as db:
        db.insert_shellcut(shellcut, os.getcwd())

    print(command)

def command_print(shellcut): ##############33
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

def command_z(enable): ### remove
    """Unimplemented."""
    error_message(2)


### HELPER FUNCTIONS ###
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

def load_shellcuts():####completely change
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

def write_shellcuts(): ####### might be totally unneeded
    """Write shellcuts to file.
    
    Creates appropriate directory if it doesn't exist.
    """
    F_SHELLCUTS_JSON.parent.mkdir(parents=True, exist_ok=True)

    with open(F_SHELLCUTS_JSON, 'w') as f:
        json.dump(shellcuts, f)


### START MAIN PROGRAM ### ##################################### need to be able to import
parser = Parser(add_help=False) ### get rid of the arg here
arguments, unknown = parser.parse_known_args()
shellcuts = load_shellcuts() ### probably dont need to load this

# Attempts to short-circuit the program and jump if only one argument given.
if len(unknown) < 1:
    command_go(arguments.shellcut) # might have to change
    exit(0)

# Adds other flags and re-parses arguments.
parser.add_additional_arguments()
arguments, unknown = parser.parse_known_args()

# If anything unknown is passed, show help and exit.
if len(unknown) > 0:
    command_help()
    exit(0)

# This tuple associates arguments from the parser with their functions.
command_pairs = ( # there's gotta be abetter way
    (arguments.help, command_help),
    (arguments.list, command_list),
    (arguments.version, command_version),
    (arguments.init, command_init),
    (arguments.bashmarks, command_bashmarks),
    (arguments.z, command_z),
    (arguments.delete, command_delete),
    (arguments.new, command_new),
    (arguments.print, command_print))

# For each in tuple, if value is not 'None', execute associated function.
for pair in command_pairs:
    if pair[0] != None:
        # Passes value to corresponding function. Functions are designed to
        # handle this value even if they don't need it.
        pair[1](pair[0])
        break
else:
    command_help()
