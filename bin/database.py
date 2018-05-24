import sqlite3
from pathlib import Path

class Database:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        if Path(self.path).is_file():
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
        else:
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
            self.create() 

        return self

    def __exit__(self, type, value, traceback):
        self.connection.commit()
        self.connection.close()

    def flush(self):
        self.cursor.execute("DELETE FROM shellcuts")
        self.cursor.execute("DELETE FROM default_command")
        
    def create(self):
        self.cursor.execute("""CREATE TABLE shellcuts (name TEXT,
                                                  path TEXT,
                                                  command TEXT)""")
        self.cursor.execute("""CREATE TABLE default_command (enabled BOOLEAN,
                                                        command TEXT)""")
        self.toggle_default(False)

    def toggle_default(self, boolean, command=""):
        self.cursor.execute("SELECT * FROM default_command")
        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO default_command VALUES (?,?)", (boolean, command))
        else:
            self.cursor.execute("UPDATE default_command SET enabled=?", (boolean,))
            if command != "":
                self.cursor.execute("UPDATE default_command SET command=?", (command,))

    def get_default(self):
        self.cursor.execute("SELECT * FROM default_command")

        return self.cursor.fetchone()

    def insert_shellcut(self, name, path):
        if self.get_shellcut_path(name) is not None:
            self.delete_shellcut(name)

        self.cursor.execute("INSERT INTO shellcuts VALUES (?,?,?)", (name, path, ""))

    def get_shellcut_path(self, name):
        self.cursor.execute("SELECT path FROM shellcuts WHERE name=?", (name,))

        return self.cursor.fetchone()

    def get_shellcut(self, name):
        self.cursor.execute("SELECT * FROM shellcuts WHERE name=?", (name,))

        return self.cursor.fetchone()

    def get_all_shellcuts(self):
        self.cursor.execute("SELECT * FROM shellcuts")

        return self.cursor.fetchall()

    def delete_shellcut(self, name):
        self.cursor.execute("DELETE FROM shellcuts WHERE name=?", (name,))

with Database("hello.db") as database:
    '''database.insert_shellcut("hello", "~/hello")
    database.insert_shellcut("hjello", "~/jaylo")
    database.insert_shellcut("goodbye", "~/goodbye")
    database.insert_shellcut("destroyme", "~/destroyme")
    database.insert_shellcut("restinpeace", "/home/tgsachse/Dropbox/Code/Shellcuts/")
    '''
    
    database.insert_shellcut("f", "/f")
    print(database.get_shellcut_path("restinpeace"))
    print(database.get_shellcut("destroyme"))
    
    database.delete_shellcut("destroyme")
    
    print(database.get_all_shellcuts())
    
    print(database.get_default())
    database.toggle_default(True, command="clsa")
    print(database.get_default())
    database.toggle_default(False)
    print(database.get_default())
