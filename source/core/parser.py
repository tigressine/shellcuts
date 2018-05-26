import shutil
import argparse
from pathlib import Path
from .commands import command_help
""""""
class Parser(argparse.ArgumentParser):
    """Subclass of ArgumentParser.

    Necessary to override error method in ArgumentParser. Sometimes the
    ArgumentParser throws errors (if argument syntax is bad, for example) and
    in all of these cases I want the help menu to appear, instead of the
    provided error messages. This subclass also provides the ability to create
    a base argument to attempt before parsing the rest, improving speed when
    jumping.
    """
    def __init__(self, *args, **kwargs):
        """Initialize by initializing super and adding base argument."""
        super().__init__(*args, add_help=False, **kwargs)

        self.add_argument('shellcut', nargs='?', default=None)

    def add_additional_arguments(self):
        """Add flags to parser."""
        self.add_argument('-d', '--delete')
        self.add_argument('-h', '--help', action='store_true', default=None)
        self.add_argument('-l', '--list', action='store_true', default=None)
        self.add_argument('-n', '--new')
        self.add_argument('-m', '--move')
        self.add_argument('-p', '--print')
        self.add_argument('-v', '--version', action='store_true', default=None)
        self.add_argument('--init', action='store_true', default=None)
        self.add_argument('--enable-bashmarks-syntax',
                          action='store_true',
                          dest='bashmarks',
                          default=None)
        self.add_argument('--disable-bashmarks-syntax',
                          action='store_false',
                          dest='bashmarks',
                          default=None)
    
    def error(self, message):
        """Call help command in case of error."""
        command_help()
        exit(0)
