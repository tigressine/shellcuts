import unittest
import sqlite3
from pathlib import Path
from database import DatabaseConnection

class DatabaseTester(unittest.TestCase):
    """
    """
    def __init__(self, *args, **kwargs):
        """Initialize tester and set default location for database."""
        super().__init__(*args, **kwargs)

        self.path = "/tmp/TestDatabase.db"

    def setUp(self):
        """Delete database from previous test."""
        if Path(self.path).is_file():
            Path(self.path).unlink()

    def testCreateNewDatabase(self):
        """Create a new database where one doesn't exist.'"""
        with DatabaseConnection(self.path) as db:
            self.assertTrue(Path(self.path).is_file())
            try:
                db.cursor.execute("SELECT * FROM table_defaults")
            except sqlite3.OperationalError:
                self.fail("Database not valid.")

    def testLoadExistingDatabase(self):
        """Create a database and then reopen and confirm data is still there."""
        populateTestingDatabase(self.path)

        with DatabaseConnection(self.path) as db:
            self.assertIsNotNone(db.get_shellcut("Test1"))
            self.assertIsNotNone(db.get_shellcut("Test2"))
            self.assertIsNone(db.get_shellcut("Test4"))

    def testInsertIntoDatabase(self):
        """Insert data into a database."""
        with DatabaseConnection(self.path) as db:
            db.insert_shellcut("Test", "/tmp/test/")
            self.assertIsNotNone(db.get_shellcut("Test"))

    def testRemoveFromDatabase(self):
        """Delete data from a database."""
        with DatabaseConnection(self.path) as db:
            db.insert_shellcut("Test", "/tmp/test/")
            db.delete_shellcut("Test")
            self.assertIsNone(db.get_shellcut("Test"))

    def testFlushDatabase(self):
        """Populate a database and then flush the data."""
        populateTestingDatabase(self.path)

        with DatabaseConnection(self.path) as db:
            db.flush()
            self.assertIsNone(db.get_shellcut("Test1"))
            self.assertIsNone(db.get_shellcut("Test2"))

    def testDefaultDisabledInNew(self):
        """Check a new database's default command flag.'"""
        with DatabaseConnection(self.path) as db:
            db.cursor.execute("SELECT enabled FROM table_defaults")
            self.assertEqual(db.cursor.fetchone()[0], 0)

    def testToggleDefaults(self):
        """Toggle default command flag for database."""
        with DatabaseConnection(self.path) as db:
            self.assertEqual(db.check_default_command_enabled(), 0)
            
            db.set_default_command(True)
            
            self.assertEqual(db.check_default_command_enabled(), 1)

    def testChangeDefaultCommand(self):
        """Change default command."""
        with DatabaseConnection(self.path) as db:
            # Check that the default command is nothing at first.
            db.set_default_command(False)
            self.assertEqual(db.get_default_command(), None)

            # Check that the default command is updated when toggled on.
            db.set_default_command(True, command="echo 'hello'")
            self.assertEqual(db.get_default_command(), "echo 'hello'")

            # Check that the default command persists even when toggled off.
            # Ignores command passed if toggling to false.
            db.set_default_command(False, "pwd")
            self.assertEqual(db.get_default_command(), "echo 'hello'")

    def testSetFollowCommand(self):
        """Set follow commands for some shellcuts."""
        populateTestingDatabase(self.path)

        with DatabaseConnection(self.path) as db:
            db.set_shellcut_command("Test1", "clsa")
            db.set_shellcut_command("Test2", "clsa; pwd")
            db.set_shellcut_command("Test3", None)

            self.assertEqual(db.get_shellcut_command("Test1"), "clsa")
            self.assertEqual(db.get_shellcut_command("Test2"), "clsa; pwd")
            self.assertEqual(db.get_shellcut_command("Test3"), None)

    def testGetFollowCommand(self):
        """Get follow commands before and after default commands enabled."""
        populateTestingDatabase(self.path)

        with DatabaseConnection(self.path) as db:
            self.assertEqual(db.check_default_command_enabled(), 0)
            db.set_shellcut_command("Test1", "clsa")
            db.set_shellcut_command("Test2", "clsa; pwd")
            db.set_shellcut_command("Test3", None)

            self.assertEqual(db.get_shellcut_command("Test1"), "clsa")
            self.assertEqual(db.get_shellcut_command("Test2"), "clsa; pwd")
            self.assertEqual(db.get_shellcut_command("Test3"), None)

            db.set_default_command(True, command="ls -A")
            self.assertEqual(db.check_default_command_enabled(), 1)
            self.assertEqual(db.get_shellcut_command("Test1"), "clsa")
            self.assertEqual(db.get_shellcut_command("Test2"), "clsa; pwd")
            # The return command for Test3 changes because default overrides
            # any None commands.
            self.assertEqual(db.get_shellcut_command("Test3"), "ls -A")

    def testInitialFollowCommands(self):
        """Test that initial follow commands are set to None."""
        populateTestingDatabase(self.path)

        with DatabaseConnection(self.path) as db:
            self.assertEqual(db.get_shellcut_command("Test1"), None)
            self.assertEqual(db.get_shellcut_command("Test2"), None)
            self.assertEqual(db.get_shellcut_command("Test3"), None)

def populateTestingDatabase(path):
    """Populate a database for testing."""
    with DatabaseConnection(path) as db:
        db.insert_shellcut("Test1", "/tmp/test1/")
        db.insert_shellcut("Test2", "/tmp/test2/")
        db.insert_shellcut("Test3", "/tmp/test3/")

if __name__ == '__main__':
    unittest.main()
