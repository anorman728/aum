#!/usr/bin/python3

# AUM: Andrew's Urgency Manager.

import sys
sys.path.insert(0, './backend')
from AumDbMan import AumDbMan

# "Main method" script.  I don't know what they call it for Python.

# Import the Aum Database Manager.
#importlib.import_module('./src/AumDbMan.py')

# Initialize database object.
testObj = AumDbMan()

# Destroy database object.
del testObj
