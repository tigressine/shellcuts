"""
"""
import argparse
from core import utilities

class Parser(argparse.ArgumentParser):
    """
    """
    def __init__(self, *args, **kwargs):
        """Initialize by initializing super and adding base argument."""
        super().__init__(*args, add_help=False, **kwargs)
        self.add_argument('name', nargs='?', default=None)


    def parse_arguments(self):
        """"""
        self.arguments, self.unknown = self.parse_known_args()


    def has_unknown_arguments(self):
        """"""
        return True if len(self.unknown) > 0 else False


    def add_arguments(self):
        """Add flags to parser."""
        self.add_argument('-n', '--new')
        self.add_argument('-m', '--move')
        self.add_argument('-p', '--print')
        self.add_argument('-d', '--delete')
        self.add_argument('--man', action='store_true', default=None)
        self.add_argument('--version', action='store_true', default=None)
        self.add_argument('-h', '--help', action='store_true', default=None)
        self.add_argument('-l', '--list', action='store_true', default=None)


    def error(self, message):
        """Call help command in case of error."""
        utilities.throw_help()
