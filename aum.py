#!/usr/bin/python3

# AUM: Andrew's Urgency Manager.

# Import modules.
import pprint # Temporary.
import sys

# Import classes from other files.
sys.path.insert(0, './backend')
from AumForm import AumForm

# "Main method" script.  I don't know what they call it for Python.

# Initialize database object.
aumFormObj = AumForm()

# START TEST CODE

pp = pprint.PrettyPrinter(indent=4)
#aumFormObj.addIssue('aumform test issue', 4)
#aumFormObj.closeIssue(8)
#aumFormObj.changePiv(8, 5)
aumFormObj.changeEffectiveStartDate(6, '6/1/2018')
#aumFormObj.addComment(8, 'test comment for aumform')
#aumFormObj.displayIssue(8)
#aumFormObj.clearClosed()
aumFormObj.listAll()

# END TEST CODE

# Destroy database object.
del aumFormObj

print("Done.") # Delete this when done writing main script.
