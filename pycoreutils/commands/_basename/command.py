from __future__ import print_function, unicode_literals

import sys

from ..base import BaseCommand


class Command(BaseCommand):
    name = 'basename'
    description = 'Print NAME with any leading directory components removed.'
    help_text = 'Remove leading directory from names'
    usage = '{} [options] NAME [NAME2]...'.format(name)

    def setup(self):
        # This command differs from its GNU alternative in that -a is assumed
        self.parser.add_argument('-z', '--zero', action='store_true', dest='zero', help='end each output line with NUL, not newline')
        self.parser.add_argument('-s', '--suffix', dest='suffix', help='remove a trailing SUFFIX as well', default='')
        self.parser.add_argument('names', metavar='NAME', nargs='+')
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        line_ending = '\n'
        if args.zero:
            line_ending = '\0'

        for name in args.names:
            sys.stdout.write('{}{}'.format(self.get_base_name(name, args.suffix), line_ending))

        return 0

    def get_base_name(self, name, suffix):
        base_name = name.split('/')[-1]
        if base_name.endswith(suffix) and len(suffix) > 0:
            base_name = base_name[:-len(suffix)]

        return base_name
