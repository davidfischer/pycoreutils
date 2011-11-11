# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

# Based on repeat.py by Guido van Rossum

from __future__ import print_function, unicode_literals
import curses
import os
import sys
import time


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    p.set_defaults(func=func)
    p.description = "execute a program periodically, showing output fullscreen"
    p.add_argument('command', nargs='+')
    p.add_argument("-n", "--interval", dest="seconds", type=float, default=2,
            help="Interval between updates")
    return p


def func(args):
    cmd = " ".join(args.command)
    cmd_really = cmd + " 2>&1"
    p = os.popen(cmd_really, "r")
    text = p.read()
    sts = p.close()
    text = addsts(args.seconds, cmd, text, sts)
    w = curses.initscr()
    try:
        while True:
            w.erase()
            try:
                w.addstr(text)
            except curses.error:
                pass
            w.refresh()
            time.sleep(args.seconds)
            p = os.popen(cmd_really, "r")
            text = p.read()
            sts = p.close()
            text = addsts(args.seconds, cmd, text, sts)
    finally:
        curses.endwin()


def addsts(interval, cmd, text, sts):
    now = time.strftime("%H:%M:%S")
    text = "%s, every %g sec: %s\n%s" % (now, interval, cmd, text)
    if sts:
        msg = "Exit status: %d; signal: %d" % (sts >> 8, sts & 0xFF)
        if text and not text.endswith("\n"):
            msg = "\n" + msg
        text += msg
    return text
