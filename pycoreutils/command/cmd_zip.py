# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import sys
import zipfile


def zip(p):
    p.set_defaults(func=func)
    p.description = "package and compress (archive) files"
    p.usage = '%(prog)s -l [OPTION]... ZIPFILE...\n' + \
       '       %(prog)s -t [OPTION]... ZIPFILE...\n' + \
       '       %(prog)s -e [OPTION]... ZIPFILE TARGET\n' + \
       '       %(prog)s -c [OPTION]... ZIPFILE SOURCE...\n'
    p.add_argument('FILE', nargs='+')
    p.add_argument('target', nargs='?')
    p.add_argument("-c", "--create", action="store_true", dest="create",
                   help="create zipfile from source.")
    p.add_argument("-e", "--extract", action="store_true", dest="extract",
                   help="extract zipfile into target directory.")
    p.add_argument("-l", "--list", action="store_true", dest="list",
                   help="list files in zipfile.")
    p.add_argument("-t", "--test", action="store_true", dest="test",
                   help="test if a zipfile is valid.")
    return p


def func(args):
    if args.list:
        if len(args) != 1:
            p.print_usage(sys.stderr)
            sys.exit(1)
        zf = zipfile.ZipFile(args[0], 'r')
        zf.printdir()
        zf.close()

    elif args.test:
        if len(args) != 1:
            p.print_usage(sys.stderr)
            sys.exit(1)
        zf = zipfile.ZipFile(args[0], 'r')
        badfile = zf.testzip()
        if badfile:
            sys.stderr("Error on file {0}\n".format(badfile))
            sys.exit(1)
        else:
            print("{0} tested ok".format(args[0]) + "\n")
            sys.exit(0)

    elif args.extract:
        if len(args) != 2:
            p.print_usage(sys.stderr)
            sys.exit(1)

        zf = zipfile.ZipFile(args[0], 'r')
        out = args[1]
        for path in zf.namelist():
            if path.startswith('./'):
                tgt = os.path.join(out, path[2:])
            else:
                tgt = os.path.join(out, path)

            tgtdir = os.path.dirname(tgt)
            if not os.path.exists(tgtdir):
                os.makedirs(tgtdir)
            fp = open(tgt, 'wb')
            fp.write(zf.read(path))
            fp.close()
        zf.close()

    elif args.create:
        if len(args) < 2:
            p.print_usage(sys.stderr)
            sys.exit(1)

        def addToZip(zf, path, zippath):
            if os.path.isfile(path):
                zf.write(path, zippath, zipfile.ZIP_DEFLATED)
            elif os.path.isdir(path):
                for nm in os.listdir(path):
                    addToZip(zf, os.path.join(path, nm),
                             os.path.join(zippath, nm))
            else:
                pycoreutils.StdErrException("Can't store {0}".format(path))

        zf = zipfile.ZipFile(args[0], 'w', allowZip64=True)
        for src in args[1:]:
            addToZip(zf, src, os.path.basename(src))

        zf.close()

    else:
        p.print_usage(sys.stderr)
        sys.exit(1)
