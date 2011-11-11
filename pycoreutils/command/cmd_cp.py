# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import os.path
import shutil


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    p.set_defaults(func=func)
    p.description = "Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY."
    p.add_argument('SOURCE', nargs='+')
    p.add_argument('DIRECTORY', nargs=1)
    p.add_argument("-i", "--interactive", action="store_true",
                   dest="interactive", help="prompt before overwrite")
    p.add_argument("-p", "--preserve", action="store_true", dest="preserve",
                   help="preserve as many attributes as possible")
    p.add_argument("-r", "-R", "--recursive", action="store_true",
                   dest="recursive", help="copy directories recursively")
    p.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                   help="print a message for each created directory")
    return p


def func(args):
    # Set the _copy function
    if args.preserve:
        _copy = shutil.copy2
    else:
        _copy = shutil.copy

    dstbase = args.pop()
    for src in args.SOURCE:
        if args.recursive:
            # Create the base destination directory if it does not exists
            if not os.path.exists(dstbase):
                os.mkdir(dstbase)

            # Walk the source directory
            for root, dirnames, filenames in os.walk(src):
                if root == dstbase:
                    continue
                dstmid = root.lstrip(src)

                # Create subdirectories in destination directory
                for subdir in dirnames:
                    srcdir = os.path.join(root, subdir)
                    dstdir = os.path.join(dstbase, dstmid, subdir)
                    if not os.path.exists(dstbase):
                        os.mkdir(dstdir)
                    if args.verbose:
                        print("'{0}' -> '{1}'".format(root, dstdir))

                # Copy file
                for filename in filenames:
                    dstfile = os.path.join(dstbase, dstmid, filename)
                    srcfile = os.path.join(root, filename)
                    if args.interactive and os.path.exists(dstfile):
                        q = input("{0}: {1} already ".format(prog, dstfile) +\
                                  "exists; do you wish to overwrite (y or n)?")
                        if q.upper() != 'Y':
                            pycoreutils.StdOutException("not overwritten", 2)
                            continue
                    _copy(srcfile, dstfile)
                    if args.verbose:
                        print("'{0}' -> '{1}'".format(srcfile, dstfile))
        else:
            dstfile = dstbase
            if os.path.isdir(dstbase):
                dstfile = os.path.join(dstbase, src)
            _copy(src, dstfile)
            if args.verbose:
                print("'{0}' -> '{1}'".format(src, dstfile))
