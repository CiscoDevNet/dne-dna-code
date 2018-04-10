#!/usr/bin/env python
"""Demonstrate module vs. locally scoped variables."""


# Create a module variable
module_variable = "I am a module variable."


# Define a function that expects to receive a value for an argument variable
def my_function(argument_variable):
    """Showing how module, argument, and local variables are used."""
    # Create a local variable
    local_variable = "I am a local variable."

    print(module_variable, "...and I can be accessed inside a function.")
    print(argument_variable, "...and I can be passed to a function.")
    print(local_variable, "...and I can ONLY be accessed inside a function.")


# Call the function; supplying the value for the argument variable
my_function(argument_variable="I am a argument variable.")


# Let's try accessing that local variable here at module scope
print("\nTrying to access local_variable outside of its function...")
try:
    print(local_variable)
except NameError as error:
    print(error)
