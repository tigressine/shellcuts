"""Print shell commands based on given arguments.

All printed commands are captured and evaluated by the shell script that calls
this file. This method is necessary because the 'cd' command moves the user
only if it is called by the user (or a shell script that the user has directly
invoked). Any calls in Python programs to 'cd', or even system calls to 'chdir',
will change the working directory of the program but not the user.

Part of Shellcuts by Tiger Sachse.
"""
import os
from pathlib import Path
from core import utilities
from core.jsonary import Jsonary

class Commander:
    """A class that holds all possible commands for Shellcuts."""
    def __init__(self, shellcuts_file, variables_file, version_file, manual_file):
        """Initialize with external, saved information.
        
        The jsonary loads shellcuts from an external JSON file into a
        dictionary structure.
        """
        self.manual_file = manual_file
        self.version_file = version_file
        self.shellcuts = Jsonary(shellcuts_file)
        self.variables = Jsonary(variables_file)


    def execute(self, arguments):
        """Call the appropriate function based on given arguments."""
        if arguments.new:
            self.new(*arguments.new)
        elif arguments.delete:
            self.delete(arguments.delete)
        elif arguments.move:
            self.move(arguments.move)
        elif arguments.list:
            self.list()
        elif arguments.print:
            self.print(arguments.print)
        elif arguments.help:
            utilities.throw_help()
        elif arguments.version:
            self.display_version()
        elif arguments.man:
            self.display_manual()
        elif arguments.follow:
            self.follow(*arguments.follow)
        elif arguments.unfollow:
            self.unfollow(arguments.unfollow)
        elif arguments.crumb:
            self.add_crumb()


    def delete(self, name):
        """Delete a shellcut from the jsonary."""
        command = 'printf "Deleted shellcut \'{0}\'\n"'

        del self.shellcuts[name]
        self.shellcuts.write()

        print(command.format(name))


    def go(self, name):
        """Change the user's directory based on a saved shellcut."""
        command = 'cd "{0}"'

        if name is None:
            utilities.throw_help()
        elif name not in self.shellcuts:
            utilities.throw_error('DoesNotExist')
        elif not Path(self.shellcuts[name][utilities.PATH]).exists():
            del self.shellcuts[name]
            utilities.throw_error('BadPath')
        else:
            path, follow = self.shellcuts[name]

            if follow is None:
                print(command.format(path))
            else:
                print(command.format(path) + '; {0}'.format(follow))


    def list(self):
        """List all saved shellcuts."""
        command = 'printf "'

        if len(self.shellcuts) > 0:
            command += 'SHELLCUTS\n'
            for name, details in self.shellcuts:
                command += '{0} : {1}\n'.format(name, details[utilities.PATH])
        else:
            command += '(No shellcuts yet. Create some with the -n flag!)\n'

        command += '"'
        print(command)


    def move(self, name):
        """Move an existing shellcut to the current working directory."""
        command = 'printf "Moved shellcut \'{0}\'\n"'

        self.shellcuts[name][utilities.PATH] = os.getcwd()
        self.shellcuts.write()
        
        print(command.format(name))


    def new(self, name, follow=None, *args):
        """Create a new shellcut."""
        command = 'printf "Added new shellcut \'{0}\'\n"'

        self.shellcuts[name] = (os.getcwd(), follow)
        self.shellcuts.write()

        print(command.format(name))


    def print(self, name):
        """Print a specific shellcut."""
        command = 'printf "{0} : {1} : {2}\n"'

        if name not in self.shellcuts:
            utilities.throw_error("DoesNotExist")
        else:
            path, follow = self.shellcuts[name]
            print(command.format(name, path, follow))


    def display_version(self):
        """Print the version information for Shellcuts."""
        command = 'printf "'

        try:
            with open(str(self.version_file), 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            utilities.throw_error('NoVersion')

        for line in lines:
            command += line
        command += '"'

        print(command)


    def display_manual(self):
        """Open the manual page for Shellcuts."""
        command = 'man -l "{0}"'.format(str(self.manual_file))
        print(command)


    def follow(self, name, follow=None, *args):
        """Add a follow command to a specific shellcut."""
        command = 'printf "Added \'{0}\' follow command to shellcut \'{1}\'\n"'

        # Throw the help menu if not enough arguments are provided.
        if follow is None:
            utilities.throw_help()

        if name not in self.shellcuts:
            utilities.throw_error('DoesNotExist')
        elif not Path(self.shellcuts[name][utilities.PATH]).exists():
            del self.shellcuts[name]
            utilities.throw_error('BadPath')
        else:
            self.shellcuts[name][utilities.FOLLOW] = follow
            self.shellcuts.write()

            print(command.format(follow, name))


    def unfollow(self, name):
        """Remove a follow command from a shellcut."""
        command = 'printf "Removed \'{0}\' follow command from shellcut \'{1}\'\n"'

        if name not in self.shellcuts:
            utilities.throw_error('DoesNotExist')
        elif not Path(self.shellcuts[name][utilities.PATH]).exists():
            del self.shellcuts[name]
            utilities.throw_error('BadPath')
        else:
            old_follow = self.shellcuts[name][utilities.FOLLOW]
            self.shellcuts[name][utilities.FOLLOW] = None
            self.shellcuts.write()

            print(command.format(old_follow, name))


    def add_crumb(self):
        """"""
        command = 'printf "Added a bread crumb at this location.\n"'

        self.variables['crumb'] = os.getcwd()
        self.variables.write()

        print(command)
