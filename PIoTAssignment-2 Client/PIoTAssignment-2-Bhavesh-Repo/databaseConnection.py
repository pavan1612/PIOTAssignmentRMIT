import sqlite3

class databaseConnection:
    def getConnection(self):
        dbname='local_database.db'
        connect = sqlite3.connect(dbname)   #This statement is used to open a connection to database
        return connect