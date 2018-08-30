import os
from pathlib import Path
from utilities import extras
from utilities.reader import Reader

class Commander:
    """"""
    def __init__(self, version_file, reader_file):
        """"""
        self.version_file = version_file
        self.reader = Reader(reader_file)


    def execute_command(self, arguments):
        pass
    

    def delete(self, name):
        command = 'printf "Deleted shellcut \'{0}\'\n"'
        self.reader.delete_shellcut(name)
        print(command.format(name))


    def go(self, name):
        command = 'cd "{0}"'
        shellcut = self.reader.get_shellcut(name)
        if shellcut is None:
            extras.throw_error("DoesNotExist")
        elif not Path(shellcut.path).exists():
            self.reader.delete_shellcut(shellcut.name)
            extras.throw_error("BadPath")
        else:
            print(command.format(shellcut.path))
    

    def list(self):
        """"""
        command = 'printf "'

        shellcuts = self.reader.get_all_shellcuts()
        if shellcuts is not None and len(shellcuts) > 0:
            command += 'SHELLCUTS\n'
            for shellcut in shellcuts:
                command += '{0} : {1}\n'.format(shellcut.name, shellcut.path)
        else:
            command += '(No shellcuts yet. Create some with the -n flag!)\n'

        command += '"'
        print(command)

    
    def move(self, name):
        """"""
        command = 'printf "Moved shellcut \'{0}\'\n"'
        self.reader.delete_shellcut(name)
        self.reader.add_shellcut(name, os.getcwd())
        print(command.format(name))

    
    def new(self, name):
        """"""
        command = 'printf "Added new shellcut \'{0}\'\n"'
        self.reader.add_shellcut(name, os.getcwd())
        print(command.format(name))


    def print(self, name):
        """"""
        command = 'printf "{0} : {1}\n"'
        shellcut = self.reader.get_shellcut(name)
        if shellcut is None:
            extras.throw_error("DoesNotExist")
        else:
            print(command.format(shellcut.name, shellcut.path))


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
