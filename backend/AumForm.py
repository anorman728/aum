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
        print("Closed issue #" + str(id) + ', "' + issueDum['issue'] + '.')

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
        self.aumDbMan.addComment(id, comment)
        print('Added comment to issue #' + str(id) + " ("
        + issueDum['issue'] + '): "' + comment + '".')

    def displayIssue(self, id):
        issue = self.aumDbMan.getIssue(id)
        dispStr = '' # To make following lines interchangeable.

        # Todo: There's probably a "space adding thingamajig" that could
        # calculate the number of spaces needed.
        dispStr+= '#' + str(id) + '        : ' + issue['issue'] + '\n'
        dispStr+= 'Added     : ' + self._formatDate(issue['added_date']) + '\n'
        dispStr+= 'Start date: ' + self._formatDate(issue['effective_start_date']) + '\n'
        dispStr+= 'Open?     : ' + ('Yes' if issue['open'] == 1 else 'No') + '\n'
        dispStr+= 'Initial   : ' + str(issue['priority_initial_value']) + '\n'
        dispStr+= 'Priority  : ' + str(issue['priority']) + '\n'
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
        dispStr = '\n'

        for issue in allIssues:
            dispStr+= "#" + str(issue['id']) + ": " + issue['issue'] + '\n'
            dispStr+= "Date : " + self._formatDate(issue['effective_start_date']) + '\n'
            dispStr+= "Priority : " + str(issue['priority_level']) + '\n'
            dispStr+= "---------\n"
            # Skipping comments.  For the moment, this should only be listed
            # when receiving one issue.
            # Todo: Make spaces equal.
        print(dispStr)


    # Helper functions below this line.

    def _getIssue(self, id):
        """Helper function just to get an issue for printing output."""
        return self.aumDbMan.getIssue(id, False)

    def _formatDate(self, inputStr):
        return datetime.utcfromtimestamp(inputStr).strftime('%m/%d/%Y')
