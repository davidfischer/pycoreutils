# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

'''
This module contains various helper-functions for pycoreutils.command
'''

import fileinput
import glob
import os
import pycoreutils
import signal
import stat
import sys


def filelist2fds(filelist, mode='r'):
    '''
    Take a list of files and yield the file descriptor.
    Yield sys.stdin if the filename is `-`, or the filelist is empty.
    Unix-style patterns will be parsed.

    So for example:::

       filelist2fds(["README.txt", "*.py", "-"])

    could yield:::

       <_io.TextIOWrapper name='README.txt' mode='r' encoding='UTF-8'>
       <_io.TextIOWrapper name='setup.py' mode='r' encoding='UTF-8'>
       <_io.TextIOWrapper name='test.py' mode='r' encoding='UTF-8'>
       <_io.TextIOWrapper name='<stdin>' mode='r' encoding='UTF-8'>

    :param filelist: A list for files
    :param mode:     Mode in which the file is opened
    '''
    filelist = filelist or ['-']
    for f in filelist:
        if f == '-':
            yield sys.stdin
        for filename in glob.iglob(f):
            if filename:
                with open(filename, mode) as fd:
                    yield fd
            else:
                print("Cannot access {1}:".format(filename) +\
                      "No such file or directory")


def getcurrentusername():
    '''
    Returns the username of the current user
    '''
    if 'USER' in os.environ:
        return os.environ['USER']      # Unix
    if 'USERNAME' in os.environ:
        return os.environ['USERNAME']  # Windows


def getsignals():
    '''
    Return a dict of all available signals
    '''
    signallist = [
        'ABRT', 'CONT', 'IO', 'PROF', 'SEGV', 'TSTP', 'USR2', '_DFL', 'ALRM',
        'FPE', 'IOT', 'PWR', 'STOP', 'TTIN', 'VTALRM', '_IGN', 'BUS', 'HUP',
        'KILL', 'QUIT', 'SYS', 'TTOU', 'WINCH', 'CHLD', 'ILL', 'PIPE', 'RTMAX',
        'TERM', 'URG', 'XCPU', 'CLD', 'INT', 'POLL', 'RTMIN', 'TRAP', 'USR1',
        'XFSZ',
    ]
    signals = {}
    for signame in signallist:
        if hasattr(signal, 'SIG' + signame):
            signals[signame] = getattr(signal, 'SIG' + signame)
    return signals


def getuserhome():
    '''
    Returns the home-directory of the current user
    '''
    if 'HOME' in os.environ:
        return os.environ['HOME']      # Unix
    if 'HOMEPATH' in os.environ:
        return os.environ['HOMEPATH']  # Windows


def mode2string(mode):
    '''
    Convert mode-integer to string
    Example: 33261 becomes "-rwxr-xr-x"
    '''
    if stat.S_ISREG(mode):
        s = '-'
    elif stat.S_ISDIR(mode):
        s = 'd'
    elif stat.S_ISCHR(mode):
        s = 'c'
    elif stat.S_ISBLK(mode):
        s = 'b'
    elif stat.S_ISLNK(mode):
        s = 'l'
    elif stat.S_ISFIFO(mode):
        s = 'p'
    elif stat.S_ISSOCK(mode):
        s = 's'
    else:
        s = '-'

    # User Read
    if bool(mode & stat.S_IRUSR):
        s += 'r'
    else:
        s += '-'

    # User Write
    if bool(mode & stat.S_IWUSR):
        s += 'w'
    else:
        s += '-'

    # User Execute
    if bool(mode & stat.S_IXUSR):
        s += 'x'
    else:
        s += '-'

    # Group Read
    if bool(mode & stat.S_IRGRP):
        s += 'r'
    else:
        s += '-'

    # Group Write
    if bool(mode & stat.S_IWGRP):
        s += 'w'
    else:
        s += '-'

    # Group Execute
    if bool(mode & stat.S_IXGRP):
        s += 'x'
    else:
        s += '-'

    # Other Read
    if bool(mode & stat.S_IROTH):
        s += 'r'
    else:
        s += '-'

    # Other Write
    if bool(mode & stat.S_IWOTH):
        s += 'w'
    else:
        s += '-'

    # Other Execute
    if bool(mode & stat.S_IXOTH):
        s += 'x'
    else:
        s += '-'

    return s


def parsefilelist(filelist=None, decompress=False):
    '''
    Takes a list of files, and generates tuple containing a line and the
    filename.
    Files called `-` will be replaced with stdin.
    If decompress is defined, a file ending with `.gz` or `.bz2` is
    decompressed automatically.
    '''
    if decompress:
        openhook = fileinput.hook_compressed
    else:
        openhook = None

    # Use stdin if filelist is empty
    filelist = filelist or '-'

    for filename in filelist:
        for line in fileinput.input(filename, openhook=openhook):
            yield (line, filename)


def showbanner(width=None):
    '''
    Returns pycoreutils banner.
    The banner is centered if width is defined.
    '''
    subtext = "-= PyCoreutils version {0} =-".format(pycoreutils.__version__)
    banner = [
        " ____  _  _  ___  _____  ____  ____  __  __  ____  ____  __    ___ ",
        "(  _ \( \/ )/ __)(  _  )(  _ \( ___)(  )(  )(_  _)(_  _)(  )  / __)",
        " )___/ \  /( (__  )(_)(  )   / )__)  )(__)(   )(   _)(_  )(__ \__ \\",
        "(__)   (__) \___)(_____)(_)\_)(____)(______) (__) (____)(____)(___/",
    ]

    if width:
        ret = ""
        for line in banner:
            ret += line.center(width) + "\n"
        ret += "\n" + subtext.center(width) + "\n"
        return ret
    else:
        return "\n".join(banner) + "\n\n" + subtext.center(68) + "\n"
