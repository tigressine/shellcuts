import sqlite3

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

    @database_access_operation
    def create(self, cursor):
        cursor.execute("CREATE TABLE database (name text, path text)")

    @database_access_operation
    def insert(self, cursor, name, path):
        cursor.execute("INSERT INTO database VALUES (?,?)", (name, path))

    @database_access_operation
    def retrieve(self, cursor, name):
        cursor.execute("SELECT path FROM database where name = (?)", (name,))
        
        return cursor.fetchone()[0]

def createMe():
    database = Database("hello.db")
    database.create()
    database.insert("hello", "~/hello")
    database.insert("goodbye", "~/goodbye")
    database.insert("destroyme", "~/destroyme")
    database.insert("restinpeace", "/home/tgsachse/Dropbox/Code/Shellcuts/")

def runMe():
    database = Database("hello.db")
    print(database.retrieve("restinpeace"))

runMe()
