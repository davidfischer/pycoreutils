from __future__ import print_function, unicode_literals

import argparse
import sys

from .utils import decode, encode, COMMAND_NAME
from ..base import BaseCommand


class Command(BaseCommand):
    name = COMMAND_NAME
    description = 'Base64 encode or decode FILE or standard input, to standard output'
    help_text = 'Base64 encode or decode input'
    usage = '{} [options] [args]'.format(name)

    def setup(self):
        self.parser.add_argument(
            'fd', metavar='FILE', nargs='?', type=argparse.FileType('rb'),
            default=sys.stdin, help='a file to base64 encode or decode',
        )
        self.parser.add_argument('-d', '--decode', action='store_true', dest='decode', help='decode data')
        self.parser.add_argument(
            '-w', dest='wrap', default=76, type=int,
            help='wrap encoded lines after COLS character (default %(default)s). Use 0 to disable line wrapping',
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        if args.decode:
            return decode(args.fd)
        else:
            return encode(args.fd, args.wrap)
