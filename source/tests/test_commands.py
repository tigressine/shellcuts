"""Define a testing class for all commands in core package.

Part of Shellcuts by Tgsachse.
"""
import re
import unittest
from io import StringIO
from core.utils import *
from core.commands import *
from unittest.mock import patch

VERSION_FILE = Path('/tmp/shellcuts_version.txt')
SHELLCUTS_FILE = Path('/tmp/shellcuts_database.db')

class CommandTester(unittest.TestCase):
    """Testing class for all commands.
    
    These commands generally wrap the database operations that form the
    backbone of the whole program.
    """
    def setUp(self):
        """Method called before every test."""
        self.delete_test_database()

    def delete_test_database(self):
        """Delete test database if it exists."""
        if SHELLCUTS_FILE.is_file():
            SHELLCUTS_FILE.unlink()

    def create_test_database(self):
        """Create a test database with some sample entries."""
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            db.insert_shellcut('test1', '/tmp/test1/')
            db.insert_shellcut('test2', '/tmp/test2/')
            db.insert_shellcut('test3', '/tmp/test3/')
            db.insert_shellcut('test4', '/tmp/test4/')

    @patch('core.utils.VERSION_FILE', VERSION_FILE)
    @patch('sys.stdout', new_callable=StringIO)
    def test_000_check_version_command(self, stream):
        """Confirm that version command can open the version information.
        
        Also tests that if the information is missing, version command throws
        the NoVersion error. The first patch decorator replaces lookups of the
        constant VERSION_FILE with a custom VERSION_FILE defined in this test
        script. The second patch decorator forces called functions to print to
        the StringIO object 'stream' instead of stdout. This keeps the screen
        clean and saves the output for regex checks.
        """
        # Delete version file if it exists.
        if VERSION_FILE.is_file():
            VERSION_FILE.unlink()

        command_version()
        # Should throw the NoVersion error here.
        self.assertTrue(re.search('NoVersion', stream.getvalue()))
    
        # Create a version file with some junk in it.
        VERSION_FILE.touch()
        VERSION_FILE.write_text('Test version information.')

        command_version()
        # Should now print that junk to the screen.
        self.assertTrue(re.search('Test version information',
                                  stream.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_001_check_help_command(self, stream):
        """Confirm that the help command prints a help menu."""
        command_help()
        self.assertTrue(re.search('Shellcuts usage:', stream.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_002_check_init_command(self, stream):
        """Confirm that the init command returns the command for the init file."""
        command_init()
        self.assertTrue(re.search('python3 /usr/bin/sc-init',
                                  stream.getvalue()))

    @patch('core.commands.SHELLCUTS_FILE', SHELLCUTS_FILE)
    @patch('os.getcwd', return_value='/tmp/test1/')
    @patch('sys.stdout', new_callable=StringIO)
    def test_003_check_new_command(self, stream, mock_getcwd):
        """Confirm that the new command adds a shellcut to a database.
        
        The second patch mocks the getcwd command in the os module. When this
        command is called it will automatically return the return_value
        defined in the decorator. This return value can be manipulated later
        in the function.
        """
        command_new('test1')

        # Check that a courtesy message is printed to the screen.
        self.assertTrue(re.search('Added new shellcut \'test1\'', stream.getvalue()))

        # Check that the new shellcut is in the database.
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            self.assertEqual(db.get_shellcut('test1')[0], 'test1')
            self.assertEqual(db.get_shellcut_path('test1'), '/tmp/test1/')

        # Change the mock current working directory so a second call to
        # command_new will overwrite the old version.
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
        """Confirm that the move command moves a shellcut to a new location.
        
        This command is essentially identical to the new command.
        """
        command_move('test1')

        # Move will function as the new command if the shellcut doesn't exist.
        self.assertTrue(re.search('Moved shellcut \'test1\'', stream.getvalue()))

        # Check that the new shellcut is in the database.
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
        self.create_test_database()
        command_delete('test2')

        # Confirm that the deletion message is printed.
        self.assertTrue(re.search('Deleted shellcut \'test2\'', stream.getvalue()))

        # Confirm that only test2 was removed from the database.
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            self.assertEqual(db.get_shellcut('test1')[0], 'test1') 
            self.assertIsNone(db.get_shellcut('test2'))
            self.assertEqual(db.get_shellcut('test3')[0], 'test3')

        # Attempt to remove something from the database that isn't there.
        command_delete('test5')

        # Confirm that the deletion message shows anyway.
        self.assertTrue(re.search('Deleted shellcut \'test5\'', stream.getvalue()))

        # Confirm that nothing was deleted.
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            self.assertEqual(len(db.get_all_shellcuts()), 3)

    @patch('core.commands.SHELLCUTS_FILE', SHELLCUTS_FILE)
    @patch('sys.stdout', new_callable=StringIO)
    def test_006_check_print_command(self, stream):
        """Confirm that the print command prints correctly."""
        self.create_test_database()
        
        command_print('test1')
        
        # Confirm that the output stream contains information from test1.
        self.assertTrue(re.search('test1.*/tmp/test1/.*None', stream.getvalue()))
        
        command_print('test5')
        
        # Confirm that attempting to print something that is not in the
        # database will throw the DoesNotExist error.
        self.assertTrue(re.search('DoesNotExist', stream.getvalue()))

    @patch('core.commands.SHELLCUTS_FILE', SHELLCUTS_FILE)
    @patch('sys.stdout', new_callable=StringIO)
    def test_007_check_list_command(self, stream):
        """Confirm that the list command prints properly."""
        self.create_test_database()
        command_list()

        # Check that each of the four entries is printed into the output stream.
        for num in range(1, 5):
            self.assertTrue(re.search('test{0}.*/tmp/test{0}/.*None'.format(num),
                            stream.getvalue()))

        self.delete_test_database()
        command_list()

        # Check that if the database is empty, a helpful message appears.
        self.assertTrue(re.search('No shellcuts yet.', stream.getvalue()))

    @patch('core.commands.SHELLCUTS_FILE', SHELLCUTS_FILE)
    @patch('sys.stdout', new_callable=StringIO)
    def test_008_check_go_command(self, stream):
        """Test the multiple behaviors of the go command."""
        self.create_test_database()
        destination = Path('/tmp/test4/')
        if destination.is_dir():
            destination.rmdir()
    
        # Attempting to go to a nonexistant shellcut results in a
        # DoesNotExist error.
        command_go('test5')
        self.assertTrue(re.search('DoesNotExist', stream.getvalue()))

        # Attempting to go to a shellcut whose path does not exist throws a
        # BadPath error and deletes the shellcut from the database.
        command_go('test4')
        self.assertTrue(re.search('BadPath', stream.getvalue()))

        # Confirm that the shellcut has been deleted from the database.
        command_go('test4')
        self.assertTrue(re.search('DoesNotExist', stream.getvalue()))

        # Make the test4 path valid.
        destination.mkdir()
        # Re-add test4 to the database.
        with DatabaseConnection(SHELLCUTS_FILE) as db:
            db.insert_shellcut('test4', '/tmp/test4/')

        # Call command_go for a valid shellcut and retrieve the cd command.
        command_go('test4')
        self.assertTrue(re.search('cd "/tmp/test4/"', stream.getvalue()))

    def test_009_check_bashmarks_command(self):
        """"""
        pass
