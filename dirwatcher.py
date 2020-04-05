#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import signal
import logging
from datetime import datetime as dt
import time
import os


__author__ = 'Safia Ali'


exit_flag = False
logger = logging.getLogger(__file__)

# keys are filenames, values are last line read
watched_files = {}


def create_parser():
    """Creates Parser and sets up command line arguments"""
    parser = argparse.ArgumentParser(
        description='Watches a directory of text files for a magic string'
    )
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help='Text file extention to watch e.g. .txt, .log')
    parser.add_argument('-i', '--interval', type=float,
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


def set_logger():
    # Set up logger to print to console
    log_format = ('%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s'
                  '[%(threadName)-12s] %(message)s')
    logging.basicConfig(
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger.setLevel(logging.DEBUG)


def set_banner(run_shut_text, start_uptime_text, app_time):
    # Setup Startup/Shutdown Banner
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '   {0} {2}\n'
        '   {1} {3}\n'
        '-------------------------------------------------------------------\n'
        .format(run_shut_text, start_uptime_text, __file__, app_time)
    )


def detect_added_files(files, args):
    for file in files:
        if file.endswith(args.ext) and file not in watched_files:
            logger.info('New file: {} found in {}'.format(file, args.path))
            watched_files[file] = 0


def detect_removed_files(files, args):
    for file in list(watched_files):
        if file not in files:
            logger.info('File removed: {}'.format(file))
            watched_files.pop(file)


def scan_single_file(filename, magic_word, directory):
    pass


def watch_directory(args):
    """Watches given directory and reports when files matching the
    given extension are added or removed.  Calls find_magic to search
    present files for a given magic word"""

    directory = os.path.abspath(args.path)
    files_in_directory = os.listdir(directory)

    # Check for new files
    detect_added_files(files_in_directory, args)

    # Stop watching deleted files
    detect_removed_files(files_in_directory, args)

    # Scan watched files
    for file in watched_files:
        scan_single_file(file, args.magic, directory)


def main():
    '''parses command line and launches forever while loop'''
    args = create_parser().parse_args()

    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends either of these to my
    # process.

    # Call set_logger for set up logger to print to console
    set_logger()

    # Set start time for running app
    app_start_time = dt.now()

    # Setup Startup Banner
    set_banner('Running', 'Started on', app_start_time.isoformat())

    # log with directory name, file extension and magic text which we find
    logger.info(
        'Watching dir={} for files with extension={} containing text={}'
        .format(args.path, args.ext, args.magic))

    # Watching directory until exit_flag set true
    while not exit_flag:
        try:
            watch_directory(args)
        except OSError:
            logger.error('{} directory does not exist'.format(args.path))
            time.sleep(args.interval*2)
        except Exception as e:
            logger.error('Unhandled exception: {}'.format(e))

        time.sleep(args.interval)

    # Setup Shutdown Banner
    uptime = dt.now() - app_start_time
    set_banner('Shutting down', 'Uptime was', uptime)

    logging.shutdown()


if __name__ == '__main__':
    main()
