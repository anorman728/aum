#!/usr/bin/python3

# AUM: Andrew's Urgency Manager.

# Import modules.
import pprint
import sys

# Import classes from other files.
sys.path.insert(0, './backend')
from AumDbMan import AumDbMan

# "Main method" script.  I don't know what they call it for Python.

# Import the Aum Database Manager.
#importlib.import_module('./src/AumDbMan.py')

# Initialize database object.
dbObj = AumDbMan()

# START TEST CODE

pp = pprint.PrettyPrinter(indent=4)
#dbObj.addIssue('new issue', 1)
#dbObj.closeIssue(4)
#dbObj.changePiv(1, 1.5)
#dbObj.changeEffectiveStartDate(4, '6/1/2018')
#dbObj.addComment(4, 'issue 4 closed comment')
#pp.pprint(dbObj.listIssues())
#dbObj.listIssues()
#dbObj.clearClosed()
pp.pprint(dbObj.getIssue(1))

# END TEST CODE

# Destroy database object.
del dbObj

print("Done.") # Delete this when done writing main script.
