from datetime import datetime
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
            added_date,
            effective_start_date
        )
        VALUES(?,?,?,?)'''
        dateDum = time.time()
        cursor = self.db.cursor()
        cursor.execute(qryDum, [name, piv, dateDum, dateDum])
        self.db.commit()
        return cursor.lastrowid

    def closeIssue(self, id):
        """Close an existing issue.

        Keyword arguments:
        id -- id of issue.
        """
        qryDum = 'UPDATE issues SET open=0 WHERE id=?'
        cursor = self.db.cursor()
        cursor.execute(qryDum, [id])
        self.db.commit()

    def changePiv(self, id, piv):
        """Change priority initial value.

        Keyword arguments:
        id -- Id of issue to modify.
        piv -- New priority initial value.
        """
        qryDum = 'UPDATE issues SET priority_initial_value = ? where id = ?'
        cursor = self.db.cursor()
        cursor.execute(qryDum, [piv, id])
        self.db.commit()

    def changeEffectiveStartDate(self, id, newDate):
        """Change effective start date.

        Keyword arguments:
        id -- Id of issue to modify.
        newDate -- String of new date, format %m/%d/%Y.
        """
        qryDum = 'UPDATE issues SET effective_start_date = ? where id = ?'
        dtObj = datetime.strptime(newDate, '%m/%d/%Y')
        dtEpc = dtObj.timestamp()
        cursor = self.db.cursor()
        cursor.execute(qryDum, [dtEpc, id])
        self.db.commit()

    def addComment(self, id, comment):
        """Add a comment for an issue.

        Keyword arguments:
        id -- Id of issue to modify.
        comment -- Comment to add.

        return: id of comment
        """
        qryDum = '''INSERT INTO comments(
            issue_id,
            comment
        )
        VALUES (?, ?)
        '''
        cursor = self.db.cursor()
        cursor.execute(qryDum, [id, comment])
        self.db.commit()
        return cursor.lastrowid

    def listIssues(self):
        """ List all issues in order of priority. """
        # Getting issues and comments separately, because want comments to be an
        # array inside the return array.
        allIssues = self._listIssues_AllIssues()
        allComments = self._listIssues_AllComments()
        for comment in allComments:
            idDum = comment['issue_id']
            commentDum = comment['comment']
            allIssues[idDum]['comments'].append(commentDum)

        for issue in allIssues:
            # Todo: Add priority level.

        # Todo: Convert allIssues from dictionary to array.
        # Todo: Sort allIssuesArr by priority level.
        return allIssues


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
            added_date INTEGER,
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

    def _listIssues_AllIssues(self):
        """Get all issues."""
        qryDum = '''
            SELECT
                id,
                issue_name,
                added_date,
                effective_start_date
            FROM
                issues
            WHERE
                open = 1
        '''
        cursor = self.db.cursor()
        cursor.execute(qryDum)
        allRows = cursor.fetchall()
        returnArr = {}
        for row in allRows:
            returnArr[row[0]] = {
                'id'                       : row[0],
                'issue'                    : row[1],
                'added_date'               : row[2],
                'effective_start_date'     : row[3],
                'comments'                 : [] # This will be appended in the listIssues function.
            }

        # Todo: It'd be really useful for both this and future projects to
        # abstract the junk above to a separate function.
        return returnArr

    def _listIssues_AllComments(self):
        """Get all comments."""
        qryDum = '''
            SELECT
                comments.issue_id,
                comments.comment
            FROM
                comments
                INNER JOIN issues ON
                    issues.id = comments.issue_id
            WHERE
                issues.open = 1
        '''
        cursor = self.db.cursor()
        cursor.execute(qryDum)
        allRows = cursor.fetchall()
        returnArr = []
        for row in allRows:
            returnArr.append({
                'issue_id'  : row[0],
                'comment'   : row[1]
            })
        return returnArr
