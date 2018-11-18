#!/usr/bin/python3

# AUM: Andrew's Urgency Manager.

import sys
sys.path.insert(0, './backend')
from AumDbMan import AumDbMan

# "Main method" script.  I don't know what they call it for Python.

# Import the Aum Database Manager.
#importlib.import_module('./src/AumDbMan.py')

# Initialize database object.
dbObj = AumDbMan()

# START TEST CODE

#print(dbObj.addIssue('testissue3', 3))
#dbObj.closeIssue(2)
#dbObj.changePiv(1, 1.5)
dbObj.changeEffectiveStartDate(3, '1/1/1980')

# END TEST CODE

# Destroy database object.
del dbObj

print("Done.") # Delete this when done writing main script.
