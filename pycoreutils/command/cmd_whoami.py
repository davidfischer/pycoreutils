from __future__ import print_function, unicode_literals
import pycoreutils
import os

try:
    import pwd
except ImportError as err:
    pass


@pycoreutils.onlyunix
def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    p.set_defaults(func=func)
    p.description = "Print the user name associated with the current" + \
                    "effective user ID.\nSame as id -un."
    return p


def func(args):
    print(pwd.getpwuid(os.getuid())[0])
