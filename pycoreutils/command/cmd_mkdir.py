# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import os


def mkdir(p):
    p.set_defaults(func=func)
    p.description = "Create the DIRECTORY(ies), if they do not already " + \
                    "exist."
    p.add_argument("directory", nargs="+")
    p.add_argument("-p", "--parents", action="store_true", dest="parents",
            help="no error if existing, make parent directories as needed")
    p.add_argument("-m", "--mode", dest="mode", default=0o777,
            help="set file mode (as in chmod), not a=rwx - umask")
    p.add_argument("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")
    return p


def func(args):
    for arg in args.directory:
        if args.parents:
            # Recursively create directories. We can't use os.makedirs
            # because -v won't show all intermediate directories
            path = arg
            pathlist = []

            # Create a list of directories to create
            while not os.path.exists(path):
                pathlist.insert(0, path)
                path, tail = os.path.split(path)

            # Create all directories in pathlist
            for path in pathlist:
                os.mkdir(path, int(args.mode))
                if args.verbose:
                    print("mkdir: created directory `{0}'".format(path))
        else:
            os.mkdir(arg, int(args.mode))
            if args.verbose:
                print("mkdir: created directory `{0}'".format(arg))
