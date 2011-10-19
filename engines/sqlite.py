import os
import platform
from retriever.lib.models import Engine, no_cleanup


class engine(Engine):
    """Engine instance for SQLite."""
    name = "SQLite"
    abbreviation = "s"
    datatypes = ["INTEGER",
                 "INTEGER",
                 "REAL",
                 "REAL",
                 "TEXT",
                 "INTEGER"]
    required_opts = [["file", 
                      "Enter the filename of your SQLite database: ",
                      "sqlite.db",
                      ""]]
                      
    def create_db(self):
        """SQLite doesn't create databases; each database is a file and needs
        a separate connection."""
        return None
        
    def escape_single_quotes(self, line):
        return line.replace("'", "''")
        
    def tablename(self):
        """The database file is specifically connected to, so database.table 
        is not necessary."""
        return self.db_name + "_" + self.table.name
        
    def table_exists(self, dbname, tablename):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM " + dbname + "_" + tablename + " LIMIT 1")
            l = len(cursor.fetchall())
            connection.close()
            return l > 0
        except:
            return False
        
    def get_connection(self):
        """Gets the db connection."""
        import sqlite3 as dbapi
        self.get_input()
        return dbapi.connect(self.opts["file"])
