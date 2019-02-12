from AumDbMan import AumDbMan
from datetime import datetime

# Todo: Docstrings.
class AumForm:
    """Class to format results from AumDbMan.  (The \"view\".  Kind of.)."""
    # It's kind of a mix of controller and view, but whatevs.

    def __init__(self):
        """Constructor"""
        self.aumDbMan = AumDbMan()

    def __del__(self):
        """Destructor"""
        del self.aumDbMan


    # Public functions.

    def addIssue(self, name, piv):
        id = self.aumDbMan.addIssue(name, piv)
        print('"' + name + '" added as issue #' + str(id) + ' with initial'
        + ' priority value of ' + str(piv) + '.')

    def closeIssue(self, id):
        issueDum = self._getIssue(id)
        self.aumDbMan.closeIssue(id)
        print("Closed issue #" + str(id) + ', "' + issueDum['issue'] + '".')

    def holdIssue(self, id, hold):
        issueDum = self._getIssue(id)
        self.aumDbMan.holdIssue(id, hold)
        actionStr = "added" if hold == 1 else "removed"
        print("Hold for issue #" + str(id) + " " + actionStr + ". ("
        + issueDum['issue'] + ").")

    def changePiv(self, id, piv):
        issueDum = self._getIssue(id)
        self.aumDbMan.changePiv(id, piv)
        print("Changed priority initial value of issue #" + str(id) + " ("
        + issueDum['issue'] + ") from " + str(issueDum['priority_initial_value'])
        + " to " + str(float(piv)) + ".")

    def changeEffectiveStartDate(self, id, newDate):
        issueDum = self._getIssue(id)
        prevDateDum = self._formatDate(issueDum['effective_start_date'])
        # How am I supposed to enforce a line length limit if I can't break the
        # line?
        self.aumDbMan.changeEffectiveStartDate(id, newDate)
        print("Changed effective start date of issue #" + str(id) + " ("
        + issueDum['issue'] + ") from " + prevDateDum + " to " + newDate + ".")

    def addComment(self, id, comment):
        issueDum = self._getIssue(id)
        if (issueDum == None):
            print("Issue #" + id + " not found.")
            return

        self.aumDbMan.addComment(id, comment)
        print('Added comment to issue #' + str(id) + " ("
        + issueDum['issue'] + '): "' + comment + '".')

    def displayIssue(self, id):
        issue = self.aumDbMan.getIssue(id)
        if (issue == None):
            print("Issue #" + id + " not found.")
            return
        dispStr = '' # To make following lines interchangeable.
        priDum = issue['priority']
        priorityLvl = str(priDum) if (priDum !=0) else 'Highest'

        # Todo: There's probably a "space adding thingamajig" that could
        # calculate the number of spaces needed.
        dispStr+= '#' + str(id) + ' (' + issue['issue'] + ')\n'
        dispStr+= 'Added     : ' + self._formatDate(issue['added_date']) + '\n'
        dispStr+= 'Start date: ' + self._formatDate(issue['effective_start_date']) + '\n'
        dispStr+= 'Open?     : ' + ('Yes' if issue['open'] == 1 else 'No') + '\n'
        dispStr+= 'On hold?  : ' + ('Yes' if issue['on_hold'] == 1 else 'No') + '\n'
        dispStr+= 'Initial   : ' + str(issue['priority_initial_value']) + '\n'
        dispStr+= 'Priority  : ' + priorityLvl + '\n'
        dispStr+= 'Comments:\n'
        dispStr+= '\n'.join(issue['comments'])
        print(dispStr)

    def clearClosed(self):
        """Just calls AumDbMan.clearClosed, since main script won't have access
        to AumDbMan."""
        self.aumDbMan.clearClosed()
        print("Cleared closed issues.")

    def listAll(self):
        """Print all issues by order of priority."""
        allIssues = self.aumDbMan.listIssues()
        print(self._formatIssues(allIssues))

    def listOnHold(self):
        """Print all on-hold issues by order of priority."""
        onHoldIssues = self.aumDbMan.listOnHoldIssues()
        print(self._formatIssues(onHoldIssues))

    def help(self):
        print('Usage by example:')
        print('''
        ./aum.py # No flags.  List all issues that aren't on hold or closed..
        ./aum.py --help # Display this help file.
        ./aum.py -a -n "Issue name" -p 3 # Adds an issue with name and initial priority value of 3.
        ./aum.py -c -i 5 # Closes issue #5.
        ./aum.py -m -i 2 -p 4 # Modifies issue #2 to initial priority level 4.
        ./aum.py -m -i 2 -d '4/5/2018' # Modifies issue #2 to effective date of 4/5/2018.
        ./aum.py -t 'this is a text comment' -i 2 # Add text comment to issue 2
        ./aum.py -h 1 -i 2 # Put issue 2 on hold.
        ./aum.py -h 0 -i 2 # Take hold off issue 2.
        ./aum.py -lh # List all on hold issues.
        ./aum.py -d # Delete closed comments.
        ./aum.py -i 2 # Display issue in toto.
        ''')


    # Helper functions below this line.

    def _getIssue(self, id):
        """Helper function just to get an issue for printing output."""
        return self.aumDbMan.getIssue(id, False)

    def _formatDate(self, inputStr):
        return datetime.utcfromtimestamp(inputStr).strftime('%m/%d/%Y')

    def _formatIssues(self, issues):
        dispStr = '\n'
        for issue in issues:
            priorDum = issue['priority_level']
            priorityLvl = str(priorDum) if (priorDum != 0) else "Highest"
            dispStr+= "#" + str(issue['id']) + ": " + issue['issue'] + '\n'
            dispStr+= "Date : " + self._formatDate(issue['effective_start_date']) + '\n'
            dispStr+= "Priority : " + priorityLvl + '\n'
            dispStr+= "---------\n"
            # Skipping comments.  For the moment, this should only be listed
            # when receiving one issue.
            # Todo: Make spaces equal.
        return dispStr
