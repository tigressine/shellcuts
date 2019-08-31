"""Parser that handles arguments for Shellcuts.

Part of Shellcuts by Tiger Sachse.
"""
import argparse
from core import utilities

class Parser(argparse.ArgumentParser):
    """Class to handle command line arguments."""
    
    def __init__(self, *args, **kwargs):
        """Initialize super and add a base argument for short-circuiting."""
        super().__init__(*args, add_help=False, **kwargs)
        self.add_argument('name', nargs='?', default=None)


    def parse_arguments(self):
        """Parse known arguments and save them."""
        self.arguments, self.unknown = self.parse_known_args()


    def has_unknown_arguments(self):
        """Determine if the most recent parse found unknown arguments."""
        return True if len(self.unknown) > 0 else False


    def add_arguments(self):
        """Add flags to the parser."""
        self.add_argument('--unfollow')
        self.add_argument('-m', '--move')
        self.add_argument('-p', '--print')
        self.add_argument('-d', '--delete')
        self.add_argument('-n', '--new', nargs='+')
        self.add_argument('-f', '--follow', nargs='+')
        self.add_argument('--man', action='store_true', default=None)
        self.add_argument('--version', action='store_true', default=None)
        self.add_argument('-h', '--help', action='store_true', default=None)
        self.add_argument('-l', '--list', action='store_true', default=None)
        self.add_argument('-c', '--crumb', action='store_true', default=None)


    def error(self, message):
        """In case of an error, show the user the help menu."""
        utilities.throw_help()
