import argparse
import importlib
import sys

from .commands import commands
from .version import __version__


description = '''
Coreutils in Pure Python

 ____  _  _  ___  _____  ____  ____  __  __  ____  ____  __    ___
(  _ \( \/ )/ __)(  _  )(  _ \( ___)(  )(  )(_  _)(_  _)(  )  / __)
 )___/ \  /( (__  )(_)(  )   / )__)  )(__)(   )(   _)(_  )(__ \__ \\
(__)   (__) \___)(_____)(_)\_)(____)(______) (__) (____)(____)(___/
'''.strip()


def main():
    parser = argparse.ArgumentParser(
        argument_default='-h',
        description=description,
        epilog='See "%(prog)s COMMAND -h" to read about a specific subcommand',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage='%(prog)s [-h] COMMAND [args]',
    )
    parser.add_argument('-v', '--version', action='version', help='Show PyCoreutils version and exit', version='%(prog)s {}'.format(__version__))
    subparsers = parser.add_subparsers(
        title='Commands',
        metavar='',
    )

    # For each subcommand, import the module and setup its argument/option
    # parser with argparse
    for command_name in commands:
        mod = importlib.import_module(u'pycoreutils.commands._{}'.format(command_name))
        if hasattr(mod, 'Command'):
            getattr(mod, 'Command').setup(subparsers)

    if len(sys.argv) <= 1:
        # Handle the case where no arguments or options are passed
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    # If a subcommand was requested, call the appropriate subcommand's
    # main method
    if args.func:
        sys.exit(args.func(args))
