from __future__ import print_function, unicode_literals
from pycoreutils.hasher import hasher


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    return hasher('sha1', p)
