from __future__ import print_function, unicode_literals

import sys


class BaseCommand(object):
    # These properties should be simple properties in a subclass
    @property
    def name(self):
        raise NotImplemented('This should be defined in a subclass')

    @property
    def description(self):
        raise NotImplemented('This should be defined in a subclass')

    @property
    def help_text(self):
        raise NotImplemented('This should be defined in a subclass')

    @property
    def help(self):
        raise NotImplemented('This should be defined in a subclass')

    # These are the two methods that need to be implemented
    def setup(self):
        raise NotImplemented('This should be defined in a subclass')

    def run(self, args):
        raise NotImplemented('This should be defined in a subclass')

    def __init__(self, subparsers, **kwargs):
        self.parser = subparsers.add_parser(
            self.name,
            description=self.description,
            help=self.help_text,
            usage=self.usage,
        )
        self.kwargs = kwargs

        self.setup()

    def exit(self, message):
        if message:
            sys.exit('{}: {}'.format(self.name, message))
