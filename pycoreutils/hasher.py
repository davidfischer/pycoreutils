# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import functools
import hashlib
import pycoreutils.lib


def hasher(algorithm, p):
    '''
    :param algorithm: hash algorithm
    :param p: ArgumentParser
    '''
    def myhash(args):
        for fd in pycoreutils.lib.filelist2fds(args.FILE, 'rb'):
            hasj = hashlib.new(algorithm)
            for data in iter(functools.partial(fd.read, 128), b''):
                hasj.update(data)
            print(hasj.hexdigest() + '  ' + fd.name)

    p.set_defaults(func=myhash)
    p.description = "Print or check {0} ".format(algorithm.upper()) +\
                    "checksums. With no FILE, or when FILE is -, read " +\
                    "standard input."
    p.add_argument('FILE', nargs='*')
    return p
