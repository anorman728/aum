#!/usr/bin/python3

# AUM: Andrew's Urgency Manager.

# Import modules.
import sys

# Import classes from other files.
sys.path.insert(0, './backend')
from AumForm import AumForm

# "Main method" script.  I don't know what they call it for Python.

# Helper functions.

def getFlagVal(flag):
    argv = sys.argv
    ind = argv.index(flag)
    malInput = 'Missing argument for ' + flag + '.'

    if ind == len(argv):
        # In this case, the flag required an argument, but the flag was the last
        # thing provided.
        raise ValueError(malInput)
    returnVal = argv[ind+1]

    if (returnVal[0] == '-'):
        # Went from one flag to the next without an argument.
        raise ValueError(malInput)

    return returnVal

# Initialize database object.
aumFormObj = AumForm()

argv = sys.argv
# I don't know a better way to do this than this giant conditional.

if len(argv) == 1: # List all the things.
    aumFormObj.listAll()

elif '--help' in argv: # Show help text.
    aumFormObj.help()

elif '-a' in argv: # Add an issue.
    if ('-n' not in argv) or ('-p' not in argv):
        # Check these specially just to make error a little clearer.
        raise ValueError('Adding issue requires -n (name) and -p (priority).')
    aumFormObj.addIssue(getFlagVal('-n'), getFlagVal('-p'))

elif '-c' in argv: # Close an issue.
    aumFormObj.closeIssue(getFlagVal('-i'))

elif '-m' in argv: # Modify an issue.
    id = getFlagVal('-i')
    if '-p' in argv:
        aumFormObj.changePiv(id, getFlagVal('-p'))
    if '-d' in argv:
        aumFormObj.changeEffectiveStartDate(id, getFlagVal('-d'))
    # Note that can modify both priority and date in one command.  This wasn't
    # part of my original design, but it's not a problem.

elif '-t' in argv: # Add a text comment.
    aumFormObj.addComment(getFlagVal('-i'), getFlagVal('-t'))

elif '-lh' in argv: # List -n-hold issues.
    aumFormObj.listOnHold()

elif '-h' in argv: # Put issue on or off hold.
    id = getFlagVal('-i')
    holding = int(getFlagVal('-h'))
    aumFormObj.holdIssue(id, holding)

elif '-i' in argv: # List an issue's details.
    aumFormObj.displayIssue(getFlagVal('-i'))

elif '-d' in argv: # Clear closed issues.
    aumFormObj.clearClosed()

else:
    print('Unable to interpret input.  Missing argument(s): ' + ' '.join(argv))


# Destroy database object.
del aumFormObj
