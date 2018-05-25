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
        self.cursor.execute('DELETE FROM table_shellcuts')
        self.cursor.execute('DELETE FROM table_defaults')
        
    def create(self):
        """Create neccessary tables in database."""
        self.cursor.execute("""CREATE TABLE table_shellcuts (name TEXT,
                                                             path TEXT,
                                                             command TEXT)""")
        self.cursor.execute("""CREATE TABLE table_defaults (enabled BOOLEAN,
                                                            command TEXT)""")
        self.set_default_command(False)

    def get_default_command(self):
        """Get the default command from table_defaults."""
        self.cursor.execute('SELECT command FROM table_defaults')

        command = self.cursor.fetchone()

        return None if command is None else command[0]

    def set_default_command(self, enabled, command=None):
        """Toggle default flag in table_defaults and set command if true."""
        self.cursor.execute('SELECT * FROM table_defaults')
       
        # If the table_defaults is empty, add a new entry.
        if self.cursor.fetchone() is None:
            self.cursor.execute('INSERT INTO table_defaults VALUES (?,?)',
                                (enabled, command))
        # Else if flag is being set to true, set both flag and command.
        elif enabled is True:
            self.cursor.execute('UPDATE table_defaults SET enabled=?, command=?',
                                (enabled, command))
        # Else flag is being set to false. Ignores command.
        else:
            self.cursor.execute('UPDATE table_defaults SET enabled=?',
                                (enabled,))

    def insert_shellcut(self, name, path):
        """Insert shellcut into database."""

        # If the shellcut already exists in the table, delete it first.
        if self.get_shellcut(name) is not None:
            self.delete_shellcut(name)

        self.cursor.execute('INSERT INTO table_shellcuts VALUES (?,?,?)',
                            (name, path, None))

    def delete_shellcut(self, name):
        """Delete a shellcut from the database."""
        self.cursor.execute('DELETE FROM table_shellcuts WHERE name=?', (name,))

    def get_shellcut(self, name):
        """Get path, name, and command of named shellcut."""
        self.cursor.execute('SELECT * FROM table_shellcuts WHERE name=?',
                            (name,))

        return self.cursor.fetchone()

    def get_all_shellcuts(self):
        """Get all shellcuts in database."""
        self.cursor.execute('SELECT * FROM table_shellcuts')

        return self.cursor.fetchall()

    def get_shellcut_path(self, name):
        """Get path of named shellcut."""
        shellcut = self.get_shellcut(name)
        
        return None if shellcut is None else shellcut[1]

    def get_shellcut_command(self, name):
        """Get follow command for shellcut."""
        shellcut = self.get_shellcut(name)

        # If the fetch fails, returns None.
        if shellcut is None:
            return None
        # If the command is None and default commands are enabled, returns
        # the default command.
        elif shellcut[2] is None and self.check_default_command_enabled():
            return self.get_default_command()
        # Else returns the custom command.
        else:
            return shellcut[2]

    def set_shellcut_command(self, name, command):
        """Set follow command for shellcut."""
        self.cursor.execute('UPDATE table_shellcuts SET command=? WHERE name=?',
                            (command, name))
    
    def check_default_command_enabled(self):
        """Check if default commands are enabled."""
        self.cursor.execute('SELECT enabled FROM table_defaults')

        enabled = self.cursor.fetchone()

        return None if enabled is None else enabled[0]
