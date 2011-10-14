# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import sys


@pycoreutils.addcommand
@pycoreutils.onlyunix
def tee(p):
    p.set_defaults(func=func)
    p.description = "Copy standard input to each FILE, and also to " + \
                    "standard output."
    p.add_argument('files', nargs='*')
    p.add_argument("-a", "--append", action="store_true", dest="append",
            help="append to the given FILEs, do not overwrite")


def func(args):
    fdlist = []
    for filename in args.files:
        if args.append:
            fdlist.append(open(filename, 'a'))
        else:
            fdlist.append(open(filename, 'w'))

    for line in sys.stdin.readlines():
        sys.stdout.write(line)
        for fd in fdlist:
            fd.write(line)
