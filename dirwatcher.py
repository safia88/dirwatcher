#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import signal
import logging


__author__ = 'Safia Ali'


exit_flag = False
logger = logging.getLogger(__file__)


def create_parser():
    """Creates Parser and sets up command line arguments"""
    parser = argparse.ArgumentParser(
        description='Watches directory for target string in text files'
    )
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help='Text file extention to watch')
    parser.add_argument('-i', '--int', type=float,
                        default=1.0, help='Number of seconds between polling')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    return parser


def signal_handler(sig_num, frame):
    """Looks for signals SIGINT and SIGTERM and toggles the exit_flag"""
    global exit_flag
    signames = dict((k, v) for v, k in reversed(sorted(
        signal.__dict__.items()))
        if v.startswith('SIG') and not v.startswith('SIG_'))

    # log the associated signal name (the python3 way)
    logger.warning('Received signal: ' + signames[sig_num])

    if sig_num == signal.SIGINT or signal.SIGTERM:
        exit_flag = True


def main():
    '''parses command line and launches forever while loop'''
    args = create_parser().parse_args()

    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends either of these to my process.


if __name__ == '__main__':
    main()
