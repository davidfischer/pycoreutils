# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils.lib
import pydoc


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    p.set_defaults(func=func)
    p.description = "number lines of files"
    p.add_argument('FILE', nargs='*')
    return p


def func(args):
    text = ''
    currentfilename = ''
    for line, filename in pycoreutils.lib.parsefilelist(args.FILE):
        if len(args.FILE) > 1 and filename != currentfilename:
            currentfilename = filename
            text += "::::::::::::::\n"
            text += currentfilename + "\n"
            text += "::::::::::::::\n"
        text += line
    pydoc.pager(text)
