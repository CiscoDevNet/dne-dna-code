#!/usr/bin/env python
"""One-line summary of your script.

Multi-line description of your script (make sure you include the copyright and
license notice).


Copyright (c) 2018 Cisco and/or its affiliates.

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


import os
import sys

import ciscosparkapi


# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))


# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)
import env_lab  # noqa
import env_user  # noqa


spark = ciscosparkapi.CiscoSparkAPI(access_token=env_user.SPARK_ACCESS_TOKEN)


print(
    """
My Lab Environment:
    DNA Center Host: {dnac_host}
    DNA Center Username: {dnac_user}
    DNA Center Password: {dnac_pass}
""".format(
        dnac_host=env_lab.DNA_CENTER["host"],
        dnac_user=env_lab.DNA_CENTER["username"],
        dnac_pass=env_lab.DNA_CENTER["password"],
    )
)


print("Oh yeah... I'm also connected to Cisco Spark as:")
print(spark.people.me())

print("...and I'm posting things to the following Spark Room:")
print(spark.rooms.get(env_user.SPARK_ROOM_ID))
