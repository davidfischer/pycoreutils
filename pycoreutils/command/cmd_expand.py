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
    p.description = "Convert tabs in each FILE to spaces"
    p.add_argument('FILE', nargs='*')
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " +\
               "decompressed automatically."
    p.add_argument("-t", "--tabs", type=int, default=8,
                   help="have tabs NUMBER characters apart, not 8")
    return p


def func(args):
    for filename in pycoreutils.lib.parsefilelist(args.FILE, True):
        for line in filename:
            print(line.expandtabs(args.tabs), end='')
