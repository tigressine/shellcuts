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
        with DatabaseConnection(self.path) as db:
            db.insert_shellcut("Test1", "/tmp/test1/")
            db.insert_shellcut("Test2", "/tmp/test2/")

        with DatabaseConnection(self.path) as db:
            self.assertIsNotNone(db.get_shellcut("Test1"))
            self.assertIsNotNone(db.get_shellcut("Test2"))
            self.assertIsNone(db.get_shellcut("Test3"))

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
        with DatabaseConnection(self.path) as db:
            db.insert_shellcut("Test1", "/tmp/test1/")
            db.insert_shellcut("Test2", "/tmp/test2/")

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
            db.cursor.execute("SELECT enabled FROM table_defaults")
            self.assertEqual(db.cursor.fetchone()[0], 0)
            
            db.toggle_default_commands(True)
            
            db.cursor.execute("SELECT enabled FROM table_defaults")
            self.assertEqual(db.cursor.fetchone()[0], 1)

    def testChangeDefaultCommand(self):
        """Change default command."""
        with DatabaseConnection(self.path) as db:
            # Check that the default command is nothing at first.
            db.toggle_default_commands(False)
            self.assertEqual(db.get_default_command()[0], "")

            # Check that the default command is updated when toggled on.
            db.toggle_default_commands(True, command="echo 'hello'")
            self.assertEqual(db.get_default_command()[0], "echo 'hello'")

            # Check that the default command persists even when toggled off.
            # Ignores command passed if toggling to false.
            db.toggle_default_commands(False, "pwd")
            self.assertEqual(db.get_default_command()[0], "echo 'hello'")

    











if __name__ == '__main__':
    unittest.main()
