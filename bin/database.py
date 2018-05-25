import sqlite3
from pathlib import Path

class DatabaseConnection:
    """An SQLite database connection containing shellcuts."""
    def __init__(self, path):
        """Save path of database as self.path."""
        self.path = path

    def __enter__(self):
        """Initialize connection and cursor."""
        if Path(self.path).is_file():
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
        else:
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
            self.create()

        return self

    def __exit__(self, type, value, traceback):
        """Save changes to database and close connection."""
        self.connection.commit()
        self.connection.close()

    def flush(self):
        """Delete all data from database."""
        self.cursor.execute("DELETE FROM table_shellcuts")
        self.cursor.execute("DELETE FROM table_defaults")
        
    def create(self):
        """Create neccessary tables in database."""
        self.cursor.execute("""CREATE TABLE table_shellcuts (name TEXT,
                                                             path TEXT,
                                                             command TEXT)""")
        self.cursor.execute("""CREATE TABLE table_defaults (enabled BOOLEAN,
                                                            command TEXT)""")
        self.toggle_default_commands(False)

    def toggle_default_commands(self, enabled, command=""):
        """Toggle default flag in table_defaults and set command if true."""
        self.cursor.execute("SELECT * FROM table_defaults")
        
        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO table_defaults VALUES (?,?)",
                                (enabled, command))
        elif enabled is True:
            self.cursor.execute("UPDATE table_defaults SET enabled=?, command=?",
                                (enabled, command))
        else:
            self.cursor.execute("UPDATE table_defaults SET enabled=?",
                                (enabled,))

    def get_default_command(self):
        """Get the default command from table_defaults."""
        self.cursor.execute("SELECT command FROM table_defaults")

        return self.cursor.fetchone()

    def insert_shellcut(self, name, path):
        """Insert shellcut into database."""

        # If the shellcut already exists in the table, delete it first.
        if self.get_shellcut_path(name) is not None:
            self.delete_shellcut(name)

        self.cursor.execute("INSERT INTO table_shellcuts VALUES (?,?,?)",
                            (name, path, ""))

    def get_shellcut_path(self, name):
        """Get path of named shellcut."""
        self.cursor.execute("SELECT path FROM table_shellcuts WHERE name=?",
                            (name,))

        return self.cursor.fetchone()

    def get_shellcut(self, name):
        """Get path, name, and command of named shellcut."""
        self.cursor.execute("SELECT * FROM table_shellcuts WHERE name=?",
                            (name,))

        return self.cursor.fetchone()

    def get_all_shellcuts(self):
        """Get all shellcuts in database."""
        self.cursor.execute("SELECT * FROM table_shellcuts")

        return self.cursor.fetchall()

    def delete_shellcut(self, name):
        """Delete a shellcut from the database."""
        self.cursor.execute("DELETE FROM table_shellcuts WHERE name=?", (name,))
