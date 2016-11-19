from __future__ import print_function, unicode_literals

import argparse
import sys

from .utils import decode, encode, COMMAND_NAME
from ..base import BaseCommand


class Command(BaseCommand):
    name = COMMAND_NAME

    @classmethod
    def setup(cls, subparsers):
        p = subparsers.add_parser(
            cls.name,
            description='Base64 encode or decode FILE or standard input, to standard output',
            help='Base64 encode or decode input',
            usage='{} [options] [args]'.format(cls.name),
        )
        p.add_argument('fd', metavar='FILE', nargs='?', type=argparse.FileType('rb'),
                       default=sys.stdin, help='a file to base64 encode or decode')
        p.add_argument('-d', '--decode', action='store_true', dest='decode', help='decode data')
        p.add_argument('-w', dest='wrap', default=76, type=int,
                       help='wrap encoded lines after COLS character (default %(default)s). '
                            'Use 0 to disable line wrapping')
        p.set_defaults(func=cls.run)

    @classmethod
    def run(cls, args):
        if args.decode:
            return decode(args.fd)
        else:
            return encode(args.fd, args.wrap)
