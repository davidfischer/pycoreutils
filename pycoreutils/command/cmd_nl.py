# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import pycoreutils.lib


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    p.set_defaults(func=func)
    p.description = "number lines of files"
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " + \
               "decompressed automatically."
    p.add_argument('FILE', nargs='*')
    p.add_argument("-s", "--number-separator", dest="separator", default="\t",
            metavar="STRING", help="add STRING after (possible) line number")
    p.add_argument("-w", "--number-width", dest="width", default=6, type=int,
            metavar="NUMBER", help="use NUMBER columns for line numbers")
    return p


def func(args):
    linenr = 0
    for filename in pycoreutils.lib.parsefilelist(args.FILE):
        for line in filename:
            if line == "\n":
                print(" " * (args.width + len(args.separator)) + line, end='')
            else:
                linenr += 1
                print("{0:>{width}}{1}{2}".format(linenr, args.separator, line,
                                                width=args.width), end='')
