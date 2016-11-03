from __future__ import print_function, unicode_literals
from pycoreutils.compressor import compressor


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    return compressor(p, 'gzip', True)
