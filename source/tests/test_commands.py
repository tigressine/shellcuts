import re
import unittest
from io import StringIO
from core.utils import *
from core.commands import *
from unittest.mock import patch

VERSION_FILE = Path('/tmp/shellcuts_version.txt')
SHELLCUTS_FILE = Path('/tmp/shellcuts_database.db')

class CommandTester(unittest.TestCase):
    """"""
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)

    @patch("core.utils.VERSION_FILE", VERSION_FILE)
    @patch("sys.stdout", new_callable=StringIO)
    def test_000_get_version_error(self, stream):
        """"""
        if VERSION_FILE.is_file():
            VERSION_FILE.unlink()

        command_version()

        self.assertTrue(re.search("NoVersion", stream.getvalue()))
    
    @patch("core.utils.VERSION_FILE", VERSION_FILE)
    @patch("sys.stdout", new_callable=StringIO)
    def test_001_get_version(self, stream):
        """"""
        if VERSION_FILE.is_file():
            VERSION_FILE.unlink()
        
        VERSION_FILE.touch() 
        VERSION_FILE.write_text('Test version information.')

        command_version()

        self.assertTrue(re.search('Test version information', stream.getvalue()))

    def test_002_
