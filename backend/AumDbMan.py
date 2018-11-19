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
        # There's some inconsistency here, because changing is only precise to
        # the day, not the second, but it's just not something I care to fix.
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

        Return: id of comment
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

    def getIssue(self, id):
        """Get a single issue by id (including comments).

        Keyword arguments:
        id -- Id of issue to pull.

        Return: Dictionary of issue.
        """

        qryIss = """
        SELECT
            issues.issue_name,
            issues.priority_initial_value,
            issues.added_date,
            issues.effective_start_date,
            issues.open,
            comments.comment,
            comments.id
        FROM
            issues
            INNER JOIN comments ON
                issues.id = comments.issue_id
        WHERE issues.id = ?
        """
        cursor = self.db.cursor()
        cursor.execute(qryIss, [id])
        rowDum = cursor.fetchone()
        returnDict = {
            'issue'                    : rowDum[0],
            'priority_initial_value'   : rowDum[1],
            'added_date'               : rowDum[2],
            'effective_start_date'     : rowDum[3],
            'open'                     : rowDum[4],
            'comments'                 : [rowDum[5]] # Will be appended next.
            'priority'                 : self._buildPriorityLevel(rowDum[3], rowDum[1]),
        }
        allRows = cursor.fetchall()
        # fetchall skips the one already received in fetchone().
        for row in allRows:
            returnDict['comments'].append(row[5])

        return returnDict


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

        for i in allIssues:
            allIssues[i]['priority_level'] = self._buildPriorityLevel(
                allIssues[i]['effective_start_date'],
                allIssues[i]['priority_initial_value']
            )

        allIssuesList = self._convertToList(allIssues)
        allIssuesList = self._sortByPriority(allIssuesList)
        return allIssuesList

    def clearClosed(self):
        """ Clear the closed issues.  Just to keep the db file from getting to
        be too large and unwieldy."""

        cursor = self.db.cursor()

        # Delete closed issues.
        qryIss = 'DELETE FROM issues WHERE open = 0'
        cursor.execute(qryIss)

        # Delete comments.
        # May want to abstract the comments stuff to a different function.

        # Collect ids of comments to delete. (Can't delete via join in SQLite.)
        qryDum = '''
            SELECT comments.id FROM
                comments
                LEFT JOIN issues ON
                    comments.issue_id = issues.id
            WHERE
                issues.id is null
        '''
        cursor.execute(qryDum)
        allRows = cursor.fetchall()
        delList = []
        for row in allRows:
            delList.append(str(row[0]))

        # Delete the comments with the found ids.
        delClause = ','.join(delList)
        qryCom = 'DELETE FROM comments WHERE id in (' + delClause + ')'
        # Todo: Parameterize this.  (Not a security issue, but should anyway.)
        cursor.execute(qryCom)

        self.db.commit()


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
                priority_initial_value,
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
                'id'                        : row[0],
                'issue'                     : row[1],
                'priority_initial_value'    : row[2],
                'added_date'                : row[3],
                'effective_start_date'      : row[4],
                'comments'                  : [] # This will be appended in the listIssues function.
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

    def _buildPriorityLevel(self, startTime, piv):
        """ Build the priority level from a date (in Unix time).
        Mathematical function is IV + (By)^2, where:
            IV is the initial value.
            B is a constant to prevent growing too quickly.
            y is the amount of time passed.
        (It used to be (IV + exp(B*y) - 1), but that didn't work out.)

        Keyword arguments:
        startTime -- Effective date, in unix time.
        piv -- Priority initial value.

        Return: float
        """
        if (piv == 0): # Zero is infinite priority.
            return 0
        currentTime = time.time()
        y = currentTime - startTime
        B = 2.8935185185185185e-07 # Urgency increases by .025 on first day.
        try:
            priorityLevel = piv + (B*y)**2
        except OverflowError: #I sure hope I never have issues this old.
            priorityLevel = 0 # Zero is "infinite priority".

        return priorityLevel

    def _convertToList(self, dictInput):
        """ Convert a dictionary to a list. """
        returnList = []
        for i in dictInput:
            returnList.append(dictInput[i])
        return returnList

    def _sortByPriority(self, issueList):
        """ Sort a list of issues (formatted as dictionary). """
        # This uses bubble sort.  Hopefully there won't be crazy long lists.
        prioritizedList = issueList.copy()

        # Pull out zeros for separate list.
        zeroList = []
        listLen = len(prioritizedList) - 1
        for i in range(listLen, 0, -1):
            if (prioritizedList[i]['priority_level'] == 0):
                zeroList.append(prioritizedList[i])
                del prioritizedList[i] # Prevent from being sorted twice.

        # Bubble sort the rest
        sorted = False
        listLen = len(prioritizedList) - 1
        while not sorted:
            sorted = True # Assume true until disproven
            for i in range(0, listLen):
                # Sort by highest to lowest.
                if (prioritizedList[i]['priority_level'] < prioritizedList[i+1]['priority_level']):
                    print('catch')#dmz1
                    dumDict = prioritizedList[i]
                    prioritizedList[i] = prioritizedList[i+1]
                    prioritizedList[i+1] = dumDict
                    sorted = False
        return zeroList + prioritizedList
