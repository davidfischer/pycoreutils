from __future__ import print_function, unicode_literals


class BaseCommand(object):
    @property
    def name(self):
        raise NotImplemented('This should be defined in a subclass')

    @classmethod
    def setup(cls, subparsers):
        raise NotImplemented('This should be defined in a subclass')

    @classmethod
    def run(cls, args):
        raise NotImplemented('This should be defined in a subclass')
