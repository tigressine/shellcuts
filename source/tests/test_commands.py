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
    def setUp(self):
        """"""
        if SHELLCUTS_FILE.is_file():
            SHELLCUTS_FILE.unlink()

    @patch('core.utils.VERSION_FILE', VERSION_FILE)
    @patch('sys.stdout', new_callable=StringIO)
    def test_000_check_version_command(self, stream):
        """Confirm that command_version can open the version information.
        
        Also tests that if the information is missing, version throws the
        NoVersion error.
        """
        if VERSION_FILE.is_file():
            VERSION_FILE.unlink()

        command_version()

        self.assertTrue(re.search('NoVersion', stream.getvalue()))
    
        VERSION_FILE.touch() 
        VERSION_FILE.write_text('Test version information.')

        command_version()

        self.assertTrue(re.search('Test version information', stream.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_001_check_help_command(self, stream):
        """Confirm that the command_help prints a help menu."""
        command_help()

        self.assertTrue(re.search('Shellcuts usage:', stream.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_002_check_init_command(self, stream):
        """Confirm that command_init returns the command to run the init file."""
        command_init()

        self.assertTrue(re.search('python3 /usr/bin/sc-init', stream.getvalue()))

    @patch('core.commands.SHELLCUTS_FILE', SHELLCUTS_FILE)
    @patch('os.getcwd', return_value='/tmp/test1/')
    @patch('sys.stdout', new_callable=StringIO)
    def test_003_check_new_command(self, stream, mock_getcwd):
        """Confirm that command_new adds a shellcut to a database."""
        command_new('test1')

        # Check that a courtesy message is printed to the screen.
        self.assertTrue(re.search('Added new shellcut \'test1\'', stream.getvalue()))

        # Check that the new shellcut is there.
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            self.assertEqual(db.get_shellcut('test1')[0], 'test1')
            self.assertEqual(db.get_shellcut_path('test1'), '/tmp/test1/')

        # Change the 'current working directory,' meaning a second call to the
        # new command will overwrite the previous entry.
        mock_getcwd.return_value = '/tmp/test2/'
        
        command_new('test1')

        # Confirm that the previous entry was overwritten, and that there is
        # only one item in the database.
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            self.assertEqual(db.get_shellcut('test1')[0], 'test1')
            self.assertEqual(db.get_shellcut_path('test1'), '/tmp/test2/')
            self.assertEqual(len(db.get_all_shellcuts()), 1)

    @patch('core.commands.SHELLCUTS_FILE', SHELLCUTS_FILE)
    @patch('os.getcwd', return_value='/tmp/test1/')
    @patch('sys.stdout', new_callable=StringIO)
    def test_004_check_move_command(self, stream, mock_getcwd):
        command_move('test1')

        # Move will function as the new command if the shellcut doesn't exist.
        self.assertTrue(re.search('Moved shellcut \'test1\'', stream.getvalue()))

        # Check that the new shellcut is there.
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            self.assertEqual(db.get_shellcut('test1')[0], 'test1')
            self.assertEqual(db.get_shellcut_path('test1'), '/tmp/test1/')

        # Change the working directory.
        mock_getcwd.return_value = '/tmp/test2/'

        command_move('test1')

        # Now there should only be one shellcut pointing to the latest directory.
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            self.assertEqual(db.get_shellcut('test1')[0], 'test1')
            self.assertEqual(db.get_shellcut_path('test1'), '/tmp/test2/')
            self.assertEqual(len(db.get_all_shellcuts()), 1)

    
    @patch('core.commands.SHELLCUTS_FILE', SHELLCUTS_FILE)
    @patch('sys.stdout', new_callable=StringIO)
    def test_005_check_delete_command(self, stream):
        """Confirm that the delete command works properly."""
        # Create a database with 3 entries.
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            db.insert_shellcut('test1', '/tmp/test1')
            db.insert_shellcut('test2', '/tmp/test2')
            db.insert_shellcut('test3', '/tmp/test3')
            self.assertEqual(len(db.get_all_shellcuts()), 3)

        command_delete('test2')

        # Confirm that the deletion message is printed.
        self.assertTrue(re.search('Deleted shellcut \'test2\'', stream.getvalue()))

        # Confirm that only test2 was removed from the database.
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            self.assertEqual(db.get_shellcut('test1')[0], 'test1') 
            self.assertIsNone(db.get_shellcut('test2'))
            self.assertEqual(db.get_shellcut('test3')[0], 'test3')

        # Attempt to remove something from the database that isn't there.
        command_delete('test4')

        # Confirm that the deletion message shows anyway.
        self.assertTrue(re.search('Deleted shellcut \'test4\'', stream.getvalue()))

        # Check that nothing was deleted.
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            self.assertEqual(len(db.get_all_shellcuts()), 2)




