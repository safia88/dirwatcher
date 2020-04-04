#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


__author__ = 'Safia Ali'


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


def main():
    '''parses command line and launches forever while loop'''
    args = create_parser().parse_args()


if __name__ == '__main__':
    main()
