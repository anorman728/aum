Andrew's Urgency Manager
========================

This is an "urgency manager" that I wrote for managing issues.  Basically, I had my issues separated by three priorities-- Low, medium, and high.  What I found is that low priority issues get ignored in favor of the high priority issues until they become moot or just persist in being really irritating.

This resolves that problem by increasing the priority level of an item over time.  So, a really old low-priority issue would actually become more important than a brand-new high-priority issue.  (Usage examples below.)

I built this for myself, but decided to share here in case someone else finds it to be helpful.  As such, this README isn't really intended to help too much with troubleshooting and I'm assuming that you already know the basics of the Unix-like command line and how to run \*.py files.

It's a command-line program written in Python and requires a Python 3 interpreter.  (It won't work in Python 2.7.)  The first thing you'll want to do is make the aum.py file executable with `chmod +x ./aum.py`.

It's written in Ubuntu and expects the executable for python3 to be `/usr/bin/python3`, but you can bypass that by running it with `python3` (or `python` if that's what your distro uses for Python 3), or you can change the shebang at the beginning of aum.py. (I imagine it'd work in Windows and Mac as long as you have Python 3 installed.)

Here's an explanation by example.

First, make sure you're in the directory that contains aum.py.  And as a reminder, Python3 must be installed and executable via `/usr/bin/python3`, and you'll need to make the file executable via `chmod +x ./aum.py`, unless you want to replace `./aum.py` with either `python3 aum.py` or `python aum.py` in the commands below.

First, let's show the help text to let us know how to use aum.py.  This will be useful for reminders if you forget some of the flags.  (It also might be all the instructions you need, so you might not need the verbose descriptions in the rest of this README.)

    $ ./aum.py -h
    Usage by example:

            ./aum.py # No flags.  List all issues.
            ./aum.py -h # Display this help file.
            ./aum.py -a -n "Issue name" -p 3 # Adds an issue with name and initial priority value of 3.
            ./aum.py -c -i 5 # Closes issue #5.
            ./aum.py -m -i 2 -p 4 # Modifies issue #2 to initial priority level 4.
            ./aum.py -m -i 2 -d '4/5/2018' # Modifies issue #2 to effective date of 4/5/2018.
            ./aum.py -t 'this is a text comment' -i 2 # Add text comment to issue 2
            ./aum.py -d # Delete closed comments.
            ./aum.py -i 2 # Display issue in toto.

Now, let's add two issues:  One with priority 1 and one with priority 3.  3 is the more urgent of the two issues.

    $ ./aum.py -a -n "Respond to email from Dave." -p 1
    "Respond to email from Dave." added as issue #1 with initial priority value of 1.
    $ ./aum.py -a -n "Put try-catch around call to API." -p 3
    "Put try-catch around call to API." added as issue #2 with initial priority value of 3.

We can list all of the issues by order of priority by executing ./aum.py without any flags.

    $ ./aum.py

    #2: Put try-catch around call to API.
    Date : 11/19/2018
    Priority : 3.0000000002681646
    ---------
    #1: Respond to email from Dave.
    Date : 11/19/2018
    Priority : 1.0000000003440686
    ---------

We can already see that the priority is increasing for both issues in what little time has passed since we've added them.

Let's say that Dave sent us that email six months ago (please don't wait that long to respond to emails, btw) and we're only just now adding it, so we'll need to change the date.

    $ ./aum.py -m -i 1 -d '7/19/2018'
    Changed effective start date of issue #1 (Respond to email from Dave.) from 11/19/2018 to 7/19/2018.

(We can also change the initial value (not the current value) of the priority level by using, say, `./aum.py -m -i 1 -p 5`.  Running this would change the initial value of the priority level to 5 on issue #1.)

We can now see how it's increased in priority, since it's so old.

    $ ./aum.py

    #1: Respond to email from Dave.
    Date : 07/19/2018
    Priority : 10.562878466913556
    ---------
    #2: Put try-catch around call to API.
    Date : 11/19/2018
    Priority : 3.0000000190107015
    ---------

(Note that changing the effective date to a *future* date will not decrease the current priority level, but will actually make it higher.  This is because the growth function is quadratic, and this isn't something that I intended to take into consideration.)

We can add a special category of urgency, "Highest", by setting the priority as zero.  These will always be listed first.

    $ ./aum.py -a -n "Put out fire in break room." -p 0
    "Put out fire in break room." added as issue #3 with initial priority value of 0.

    $ ./aum.py

    #3: Put out fire in break room.
    Date : 11/19/2018
    Priority : Highest
    ---------
    #1: Respond to email from Dave.
    Date : 07/19/2018
    Priority : 10.563140800620305
    ---------
    #2: Put try-catch around call to API.
    Date : 11/19/2018
    Priority : 3.000000032506293
    ---------

We can look at a detailed view of a specific issue, as well.

    $ ./aum.py -i 3
    #3 (Put out fire in break room.)
    Added     : 11/19/2018
    Start date: 11/19/2018
    Open?     : Yes
    Initial   : 0.0
    Priority  : Highest
    Comments:
    None

We can add text comments, which will only be viewable in the detailed view of a specific issue.  You can add as many comments to an issue as you like.

    $ ./aum.py -t "Ryan started it." -i 3
    Added comment to issue #3 (Put out fire in break room.): "Ryan started it.".
    $ ./aum.py -i 3
    #3 (Put out fire in break room.)
    Added     : 11/19/2018
    Start date: 11/19/2018
    Open?     : Yes
    Initial   : 0.0
    Priority  : Highest
    Comments:
    Ryan started it.

We can close an issue using the '-c' flag.

    $ ./aum.py -c -i 3
    Closed issue #3, "Put out fire in break room.".

(There's currently no way to view closed issues or re-open an issue.  It's possible I might add that in the future if it turns out anybody uses this and is interested, but remember that I made this for myself, and if I need to reopen an issue I'd just edit the database file directly.)

Eventually, we'll have closed a lot of issues, so the database file will become large and the program will run slowly.  We can delete the closed issues permanently with the '-d' flag.

    $ ./aum.py -d
    Cleared closed issues.
