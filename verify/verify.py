#!/usr/bin/env python
"""Verify the backend lab environment.

Verify that the `env_lab.py` and `env_user.py` Python environment files exist
and that they import successfully, and then verify that the backend lab
environments are accessible and responding to API calls.


Copyright (c) 2018-21 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from importlib.util import module_from_spec, spec_from_file_location
from glob import glob
import os
import sys


# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, ".."))

# Extend the system path to include the project root
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# Verify env_lab.py
try:
    print("==> Importing env_lab")
    import env_lab  # noqa
except Exception as e:
    print("FAILED: Error importing env_lab.py; error details:\n{}\n".format(e))
    sys.exit(1)


# Verify env_user.py
try:
    print("==> Importing env_user")
    import env_user  # noqa
except ModuleNotFoundError:
    print(
        "\nFAILED: Error importing env_user.py; file not found. Did you "
        "create one? Copy and edit env_lab.template in the repository root.\n"
    )
    sys.exit(1)
except Exception as e:
    print(
        "\nFAILED: Error importing `env_user.py`. Error Details:\n"
        "{}\n".format(e)
    )
    sys.exit(1)


fail_bit = 0


if env_lab.ENVIRONMENT_IN_USE == "sandbox" or env_lab.ENVIRONMENT_IN_USE == "express" or env_lab.ENVIRONMENT_IN_USE =="custom":
    print(f"env_lab.py - ENVIRONMENT_IN_USE: {env_lab.ENVIRONMENT_IN_USE}")
else:
    print("\nImproper value inputted. go to env_lab.py and select either sandbox, express, or custom.")
    print(f"ERROR: env_lab.py - Invalid ENVIRONMENT_IN_USE: {env_lab.ENVIRONMENT_IN_USE}")
    fail_bit = 1

print(f"env_user.py - SPARK_ACCESS_TOKEN: {env_user.SPARK_ACCESS_TOKEN}")
print(f"env_user.py - SPARK_ROOM_ID: {env_user.SPARK_ROOM_ID}")
print(f"env_user.py - MERAKI_API_KEY: {env_user.MERAKI_API_KEY}\n")

# Verify backend lab environments
backend = os.path.abspath(os.path.join(here, "backend"))
verified = []
for python_file in glob(os.path.join(backend, "*.py")):
    name = os.path.splitext(os.path.basename(python_file))[0]
    spec = spec_from_file_location(name, python_file)
    module = module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        verified.append(module.verify())
    except ModuleNotFoundError:
        print("\nFAILED: Error importing module. You need to install lab requirements.  \n\tEnter Command: pip install -r requirements.txt")
        fail_bit = 1
        break
    except AttributeError:
        print("\nFAILED: Error due to invalid ENVIRONMENT_IN_USE input in the env_lab.py file. \n\tCheck to see if the environment requires VPN access.")
        fail_bit = 1
        break

if fail_bit == 1:
    print("\nCorrect Errors and rerun.\n")
elif all(verified):
    print("\nAll lab backend systems are responding.  You're good to go!\n")
else:
    print(
        "\nSome of the backend systems didn't respond or reported errors; "
        "please check the above output for details.\n"
    )
