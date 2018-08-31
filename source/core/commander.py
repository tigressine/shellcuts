"""
"""
import os
from pathlib import Path
from core import utilities
from core.jsonary import Jsonary

class Commander:
    """"""
    def __init__(self, version_file, shellcuts_file, manual_file):
        """"""
        self.manual_file = manual_file
        self.version_file = version_file
        self.shellcuts = Jsonary(shellcuts_file)


    def execute(self, arguments):
        """"""
        if arguments.delete:
            self.delete(arguments.delete)
        elif arguments.help:
            utilities.throw_help()
        elif arguments.list:
            self.list()
        elif arguments.move:
            self.move(arguments.move)
        elif arguments.new:
            self.new(arguments.new)
        elif arguments.print:
            self.print(arguments.print)
        elif arguments.version:
            self.version()
        elif arguments.man:
            self.manual()


    def delete(self, name):
        """"""
        command = 'printf "Deleted shellcut \'{0}\'\n"'
        del self.shellcuts[name]
        self.shellcuts.write()
        print(command.format(name))


    def go(self, name):
        """"""
        command = 'cd "{0}"'
        if name is None:
            utilities.throw_help()
        elif self.shellcuts[name] is None:
            utilities.throw_error("DoesNotExist")
        elif not Path(self.shellcuts[name]).exists():
            del self.shellcuts[name]
            utilities.throw_error("BadPath")
        else:
            print(command.format(self.shellcuts[name]))


    def list(self):
        """"""
        command = 'printf "'

        if len(self.shellcuts) > 0:
            command += 'SHELLCUTS\n'
            for shellcut in self.shellcuts:
                command += '{0} : {1}\n'.format(*shellcut)
        else:
            command += '(No shellcuts yet. Create some with the -n flag!)\n'

        command += '"'
        print(command)


    def move(self, name):
        """"""
        command = 'printf "Moved shellcut \'{0}\'\n"'
        del self.shellcuts[name]
        self.shellcuts[name] = os.getcwd()
        self.shellcuts.write()
        print(command.format(name))


    def new(self, name):
        """"""
        command = 'printf "Added new shellcut \'{0}\'\n"'
        self.shellcuts[name] = os.getcwd()
        self.shellcuts.write()
        print(command.format(name))


    def print(self, name):
        """"""
        command = 'printf "{0} : {1}\n"'
        if name not in self.shellcuts:
            utilities.throw_error("DoesNotExist")
        else:
            print(command.format(name, self.shellcuts[name]))


    def version(self):
        """"""
        command = 'printf "'

        try:
            with open(str(self.version_file), 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            utilities.throw_error("NoVersion")

        for line in lines:
            command += line
        command += '"'
        print(command)


    def manual(self):
        """"""
        command = 'man ".'
        command += str(self.manual_file)
        command += '"'
        print(command)
