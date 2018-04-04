#!/usr/bin/env python
"""Perform one or several checks and rollbacks configuration if check fails.

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

import argparse
import os

from cli import cli, clip
import requests


BACKUP_CONFIG_IOS_PATH = 'flash:/running-config.bak'

WEB_HOSTS = [
    'https://www.cisco.com',
    'https://www.google.com',
]


def send_syslog(message):
    """Sends a syslog message to the device with severity 6

    Args:
        message (str): message to be sent

    Returns:
        None
    """
    cli(
        'send log facility PYTHON severity 6 mnemonics CONF_CHECK '
        '{message}'.format(message=message)
    )


def parse_arguments():
    """Adds command-line argument parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--check-only', action="store_true", default=False,
        help='Do not apply the rollback if the checks fail'
    )
    parser.add_argument(
        '--syslog', action="store_true", default=False,
        help='Send syslog informational messages'
    )
    args = parser.parse_args()
    return args


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


def save_config_to_ios_file(backup_config_ios_path, syslog=False):
    """Saves the current running configuration locally to the filesystem

    Args:
        backup_config_ios_path (str): IOS path to the backup configuration
        syslog (boolean): True, if informational messages should be sent to
            the syslog

    Returns:
        None
    """
    cli('copy running-config {}\n'.format(backup_config_ios_path))

    message = ('Running configuration was saved to {}'.format(
        backup_config_ios_path
    ))
    if syslog:
        send_syslog(message)


def web_check(urls, timeout=15, syslog=False):
    """Checks HTTP connections to the list of URLs

    Args:
        urls (list): list of URLs for requests to open HTTP connection to
        timeout (int): how long in seconds requests library will wait for
            a response from the URL
        syslog (boolean): True, if informational messages should be sent to
            the syslog

    Returns:
        boolean: True, if all HTTP requests finished successfully
            False, if at least one HTTP request failed
    """
    for url in urls:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            message = 'Web check for url {url} ... passed!'.format(url=url)
            print(message)
        except requests.exceptions.RequestException as e:
            message = (
                'Web check for url {url} ... failed: '
                '{e.__class__.__name__}: {e}'.format(
                    url=url, e=e
                )
            )
            print(message)
            if syslog:
                syslog_message = (
                    'Web check for url {url} ... failed due to '
                    '{e.__class__.__name__}'.format(
                        url=url, e=e
                    )
                )
                send_syslog(syslog_message)
            return False
    else:
        message = "All web checks passed successfully!"
        print(message)
        if syslog:
            send_syslog(message)
        return True


def checks(syslog=False):
    """A batch of different checks to be performed

    Args:
        syslog (boolean): True, if informational messages should be sent to
            the syslog

    Raises:
        AssertionError: when one of the checks fails
    """
    assert web_check(WEB_HOSTS, syslog=syslog)
    # More checks can be defined here


def main():
    args = parse_arguments()
    backup_config_linux_path = convert_ios_path_to_linux(
        BACKUP_CONFIG_IOS_PATH
    )
    if args.check_only:
        checks()
    # check if the current running config backup is saved on the flash
    elif not os.path.isfile(backup_config_linux_path):
        # if not, save it and exit
        save_config_to_ios_file(BACKUP_CONFIG_IOS_PATH, args.syslog)
        message = 'Running-config file is saved for the first time, exiting.'
        print(message)
        if args.syslog:
            send_syslog(message)
    # not running for the first time, starting checks
    else:
        try:
            checks(args.syslog)
        except AssertionError:
            message = 'Trying configuration rollback'
            print(message)
            if args.syslog:
                send_syslog(message)
            clip('configure replace {config_path} force'.format(
                config_path=BACKUP_CONFIG_IOS_PATH
            ))
        else:
            save_config_to_ios_file(BACKUP_CONFIG_IOS_PATH, args.syslog)


if __name__ == '__main__':
    main()
