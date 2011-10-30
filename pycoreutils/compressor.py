# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

import bz2
import gzip
import os
import shutil
import sys


def compressor(p, comptype='gzip', decompress=False):
    '''
    Handles compression and decompression as bzip2 and gzip
    '''
    p.description = "Compress or uncompress FILEs (by default, compress " + \
                    "FILES in-place)."
    p.set_defaults(func=compressorfunc, comptype=comptype,
                   decompress=decompress)
    p.add_argument('files', nargs='*')
    p.add_argument("-c", "--stdout", "--as-stdout", action="store_true",
            dest="stdout",
            help="write on standard output, keep original files unchanged")
    p.add_argument("-C", "--compresslevel", dest="compresslevel", type=int,
            default=6, help="set file mode (as in chmod), not a=rwx - umask")
    p.add_argument("-d", "--decompress", action="store_true",
            dest="decompress", help="decompress")
    p.add_argument("-1", "--fast", action="store_const", dest="compresslevel",
            const=1, help="Use the fastest type of compression")
    p.add_argument("-2", action="store_const", dest="compresslevel", const=2,
            help="Use compression level 2")
    p.add_argument("-3", action="store_const", dest="compresslevel", const=3,
            help="Use compression level 3")
    p.add_argument("-4", action="store_const", dest="compresslevel", const=4,
            help="Use compression level 4")
    p.add_argument("-5", action="store_const", dest="compresslevel", const=5,
            help="Use compression level 5")
    p.add_argument("-6", action="store_const", dest="compresslevel", const=6,
            help="Use compression level 6")
    p.add_argument("-7", action="store_const", dest="compresslevel", const=7,
            help="Use compression level 7")
    p.add_argument("-8", action="store_const", dest="compresslevel", const=8,
            help="Use compression level 8")
    p.add_argument("-9", "--best", action="store_const", dest="compresslevel",
            const=9, help="Use the best type of compression")


def compressorfunc(args):
    if args.comptype == 'gzip':
        compresstype = gzip.GzipFile
        suffix = '.gz'
    elif args.comptype == 'bzip' or comptype == 'bzip2':
        compresstype = bz2.BZ2File
        suffix = '.bz2'

    infiles = args.files

    # Use stdin for input if no file is specified or file is '-'
    if len(args.files) == 0 or args.files == ['-']:
        infiles = [sys.stdin]

    for infile in infiles:
        print(infile)
        if args.decompress:
            # Decompress
            infile = compresstype(infile, 'rb',
                                  compresslevel=args.compresslevel)
            if len(args.files) == 0 or args.stdout:
                outfile = sys.stdout
            else:
                unzippath = infile.rstrip(suffix)
                if os.path.exists(unzippath):
                    q = input("{0}: {1} already ".format(p.prog, unzippath) + \
                              "exists; do you wish to overwrite (y or n)? ")
                    if q.upper() != 'Y':
                        StdOutException("not overwritten", 2)

                outfile = open(unzippath, 'wb')
        else:
            # Compress
            zippath = infile + suffix
            infile = open(infile, 'rb')
            if len(args) == 0 or args.stdout:
                outfile = sys.stdout
            else:
                if os.path.exists(zippath):
                    q = input("{0}: {1} already".format(p.prog, zippath) + \
                              " exists; do you wish to overwrite (y or n)? ")
                    if q.upper() != 'Y':
                        StdErrException("not overwritten", 2)

                outfile = compresstype(zippath, 'wb',
                                       compresslevel=args.compresslevel)

        shutil.copyfileobj(infile, outfile)
