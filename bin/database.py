import sqlite3
from pathlib import Path

def database_access_operation(operation):
    def wrapper(self, *args, **kwargs):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        result = operation(self, cursor, *args, **kwargs)

        connection.commit()
        connection.close()

        return result

    return wrapper

class Database:
    def __init__(self, path):
        self.path = path

        if not Path(self.path).is_file():
            self.create()

    def delete(self):
        if Path(self.path).is_file():
            Path(self.path).unlink()

    def flush(self):
        self.delete()
        self.create()

    # create new from nothing
    @database_access_operation
    def create(self, cursor):
        cursor.execute("""CREATE TABLE shellcuts (name TEXT,
                                                  path TEXT,
                                                  command TEXT)""")
        cursor.execute("""CREATE TABLE default_command (enabled BOOLEAN,
                                                        command TEXT)""")
        self.toggle_default(False)

    @database_access_operation
    def toggle_default(self, cursor, boolean, command=""):
        cursor.execute("SELECT * FROM default_command")
        if cursor.fetchone() == None:
            cursor.execute("INSERT INTO default_command VALUES (?,?)", (boolean, command))
        else:
            cursor.execute("UPDATE default_command SET enabled=?", (boolean,))
            if command != "":
                cursor.execute("UPDATE default_command SET command=?", (command,))

    @database_access_operation
    def get_default(self, cursor):
        cursor.execute("SELECT * FROM default_command")

        return cursor.fetchone()

    # add operation
    @database_access_operation
    def insert_shellcut(self, cursor, name, path):
        if self.get_shellcut_path(name) != None:
            self.delete_shellcut(name)

        cursor.execute("INSERT INTO shellcuts VALUES (?,?,?)", (name, path, ""))

    # get 1 path operation
    @database_access_operation
    def get_shellcut_path(self, cursor, name):
        cursor.execute("SELECT path FROM shellcuts WHERE name=?", (name,))

        return cursor.fetchone()

    # get shellcut
    @database_access_operation
    def get_shellcut(self, cursor, name):
        cursor.execute("SELECT * FROM shellcuts WHERE name=?", (name,))

        return cursor.fetchone()

    # get all them
    @database_access_operation
    def get_all_shellcuts(self, cursor):
        cursor.execute("SELECT * FROM shellcuts")

        return cursor.fetchall()

    # delete a shellcut
    @database_access_operation
    def delete_shellcut(self, cursor, name):
        cursor.execute("DELETE FROM shellcuts WHERE name=?", (name,))

    @database_access_operation





def createMe():
    database = Database("hello.db")
    database.flush()
    database.insert_shellcut("hello", "~/hello")
    database.insert_shellcut("hjello", "~/jaylo")

    database.insert_shellcut("goodbye", "~/goodbye")
    database.insert_shellcut("destroyme", "~/destroyme")
    database.insert_shellcut("restinpeace", "/home/tgsachse/Dropbox/Code/Shellcuts/")

def runMe():
    database = Database("hello.db")
    print(database.get_shellcut_path("restinpeace"))
    print(database.get_shellcut("destroyme"))
    print("")
    database.delete_shellcut("destroyme")
    print(database.get_all_shellcuts())
    print(database.get_default())
    database.toggle_default(True, command="clsa")
    print(database.get_default())
    database.toggle_default(False)
    print(database.get_default())

createMe()
runMe()
