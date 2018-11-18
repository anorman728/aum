import sqlite3

class AumDbMan:
    """Class to manage the Aum database.  (The \"model\")."""

    def __init__(self):
        """Constructor"""
        print('Constructor called')#Delete this when done.

        # Build the database file and set to a class var.
        self.db = sqlite3.connect('./aum.db')

        # Build queries for setting up the tables.
        qryIssues = '''CREATE TABLE IF NOT EXISTS issues(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_name TEXT,
            priority_initial_value REAL,
            start_date INTEGER,
            effective_start_date INTEGER
        )'''
        qryComments = '''CREATE TABLE IF NOT EXISTS comments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id INTEGER,
            comment TEXT
        )'''
        
        # Build the tables in the sqlite file.
        cursor = self.db.cursor();
        for cmd in [qryIssues, qryComments]:
            cursor.execute(cmd)
        self.db.commit()

    def __del__(self):
        """Destructor"""
        print('Destructor called')#Delete this when done
        self.db.close()
