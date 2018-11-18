import os
import sqlite3
import time

class AumDbMan:
    """Class to manage the Aum database.  (The \"model\")."""

    def __init__(self):
        """Constructor"""
        self._buildDatabaseFile()
        self._buildDatabase()

    def __del__(self):
        """Destructor"""
        self.db.close()


    # "Public" functions

    def addIssue(self, name, piv):
        """Add a new issue.

        Keyword arguments:
        name -- Name of issue
        piv -- Priority initial value

        Return: id of issue
        """
        qryDum = '''INSERT INTO issues(
            issue_name,
            priority_initial_value,
            start_date,
            effective_start_date
        )
        VALUES(?,?,?,?)'''
        dateDum = time.time()
        cursor = self.db.cursor()
        cursor.execute(qryDum, [name, piv, dateDum, dateDum])
        self.db.commit()
        return cursor.lastrowid


    # Helper functions below this line.

    def _buildDatabaseFile(self):
        """Build the database file and set to a class var."""
        dirPath = os.path.dirname(os.path.realpath(__file__))
        dbFile = dirPath + '/aum.db'
        self.db = sqlite3.connect(dbFile)

    def _buildDatabase(self):
        # Build queries for setting up the tables.
        qryIssues = '''CREATE TABLE IF NOT EXISTS issues(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_name TEXT,
            priority_initial_value REAL,
            start_date INTEGER,
            effective_start_date INTEGER,
            open INTEGER DEFAULT 1
        )'''
        qryComments = '''CREATE TABLE IF NOT EXISTS comments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id INTEGER,
            comment TEXT
        )'''
        
        # Build the tables in the sqlite file.
        cursor = self.db.cursor()
        for cmd in [qryIssues, qryComments]:
            cursor.execute(cmd)
        self.db.commit()
