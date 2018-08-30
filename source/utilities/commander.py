import os
from pathlib import Path
from utilities import extras
from utilities.json_dictionary import JSONDictionary

class Commander:
    """"""
    def __init__(self, version_file, shellcuts_file):
        """"""
        self.version_file = version_file
        self.shellcuts = JSONDictionary(shellcuts_file)


    def execute_command(self, arguments):
        pass
    

    def delete(self, name):
        command = 'printf "Deleted shellcut \'{0}\'\n"'
        del self.shellcuts[name]
        self.shellcuts.write()
        print(command.format(name))


    def go(self, name):
        command = 'cd "{0}"'
        if self.shellcuts[name] is None:
            extras.throw_error("DoesNotExist")
        elif not Path(self.shellcuts[name]).exists():
            del self.shellcuts[name]
            extras.throw_error("BadPath")
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
        if self.shellcuts[name] is None:
            extras.throw_error("DoesNotExist")
        else:
            print(command.format(*self.shellcuts[name]))


    def version(self):
        """"""
        command = 'printf "'
        
        try:
            with open(str(self.version_file), 'r') as f:
                lines = f.readlines()    
        except FileNotFoundError:
            extras.throw_error("NoVersion")
        
        for line in lines:
            command += line
        command += '"'
        print(command)
