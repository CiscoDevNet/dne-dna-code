#!/usr/bin/env python
"""Module docstring."""


# Imports
import os
import sys


# Module Constants
START_MESSAGE = "CLI Inspection Script"


# Module "Global" Variables
location = os.path.abspath(__file__)


# Module Functions and Classes
def main(*args):
    """My main script function.

    Displays the full patch to this script, and a list of the arguments passed
    to the script.
    """
    print(START_MESSAGE)
    print("Script Location:", location)
    print("Arguments Passed:", args)


# Check to see if this file is the "__main__" script being executed
if __name__ == '__main__':
    _, *script_args = sys.argv
    main(*script_args)
