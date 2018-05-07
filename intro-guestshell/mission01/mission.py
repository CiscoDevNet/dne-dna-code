#!/usr/bin/env python
"""Sends configuration difference to Webex Teams, formerly Spark.

Compares the current running configuration and the saved running
configuration, creates diff and sends it to a Webex Teams room.
Should be invoked after every configuration change by EEM.


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
import re

from cli import cli, clip
from ciscosparkapi import CiscoSparkAPI


BACKUP_CONFIG_IOS_PATH = 'flash:/running-config.bak'


def send_syslog(message):
    """Sends a syslog message to the device with severity 6

    Args:
        message (str): message to be sent

    Returns:
        None
    """
    cli(
        'send log facility PYTHON severity 6 mnemonics CONF_DIFF '
        '{message}'.format(message=message)
    )


def convert_ios_path_to_linux(path):
    """Convert the file path valid in IOS to the correct path in Guest Shell.

    Example:
    >>> convert_ios_path_to_linux('flash:/running-config.bak')
    '/flash/running-config.bak'

    Args:
        path(str): the path valid in IOS.
            Should contain filesystem, otherwise 'flash' is assumed
    Returns:
        string, the converted path which is valid in the Guest Shell
    """
    path_components = os.path.normpath(path).split(os.sep)
    file_system = path_components[0]

    if ':' in file_system:
        file_system = file_system.strip(':')
        path_components = path_components[1:]
    else:
        file_system = 'flash'

    result_path = os.path.join(os.sep, file_system, *path_components)
    return result_path


def save_config_to_ios_file(backup_config_ios_path):
    """Saves the current running configuration locally to the filesystem

    Args:
        backup_config_ios_path (str): IOS path to the backup configuration

    Returns:
        None
    """
    # MISSION TODO 3: replace with the function that runs IOS commands and
    # returns output instead of printing it
    MISSION('copy running-config {}\n'.format(backup_config_ios_path))
    # END MISSION SECTION 3

    message = (
        'Running configuration was saved to {}'.format(backup_config_ios_path)
    )
    print(message)
    send_syslog(message)


def get_config_diff(backup_config_ios_path):
    """Gets configuration difference using `show archive config diff` command

    Args:
        backup_config_ios_path (str): IOS path to the backup configuration

    Returns:
        list of lines containing config difference
    """
    config_diff = cli(
        'show archive config diff {} system:running-config'.format(
            backup_config_ios_path
        )
    )
    backup_config_linux_path = convert_ios_path_to_linux(
        backup_config_ios_path
    )
    os.remove(backup_config_linux_path)
    save_config_to_ios_file(backup_config_ios_path)

    if re.search('No changes were found', config_diff):
        return None
    else:
        # split lines by \r\n into a list
        config_diff_lines = re.split(r'\r?\n', config_diff)
        return config_diff_lines


def form_spark_message(config_diff_lines):
    """Creates a Spark message formatted in markdown based on config diff

    Args:
        config_diff_lines (list): list of lines containing config
            difference

    Returns:
        str: markdown Spark message as a string
    """
    message = (
        'Configuration differences between '
        'the running config and the last backup:\n'
        '```\n'
        '{}\n'
        '```\n'
        'I\'ve completed **Introduction to '
        'Guest Shell** Mission!'.format('\n'.join(config_diff_lines))
    )
    return message


def main():
    spark_api = CiscoSparkAPI()

    # MISSION TODO 4: use the function that converts IOS path to
    # linux, which is defined in this file
    backup_config_linux_path = MISSION(
        BACKUP_CONFIG_IOS_PATH
    )
    # END MISSION SECTION 4

    # MISSION TODO 5: check if the running config backup
    # under the linux path exists in the filesystem
    if not os.path.isfile(MISSION):
        # END MISSION SECTION 5

        # if not, save it and exit
        save_config_to_ios_file(BACKUP_CONFIG_IOS_PATH)
        message = 'Running-config file is saved for the first time, exiting.'
        print(message)
        send_syslog(message)
    # not running for the first time
    else:
        # MISSION TODO 6: use the function that gets configuration difference
        # between the current configuration and saved
        config_diff_lines = MISSION(BACKUP_CONFIG_IOS_PATH)
        # END MISSION SECTION 6
        if config_diff_lines is not None:
            print('Changes have been found')
            message = form_spark_message(config_diff_lines)
            spark_api.messages.create(
                roomId=os.environ.get('SPARK_ROOM_ID'),
                markdown=message,
            )
            message = 'Spark message has been sent'
            print(message)
            send_syslog(message)
        else:
            message = 'No configuration changes have been found.'
            send_syslog(message)


if __name__ == '__main__':
    main()
