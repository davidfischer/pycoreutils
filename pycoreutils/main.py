import argparse
import importlib
import sys

from .command import commands


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
    subparsers = parser.add_subparsers(title='Commands', metavar='')

    # For each subcommand, import the module and setup its argument/option
    # parser with argparse
    for command in commands:
        mod = importlib.import_module(u'pycoreutils.command._{}'.format(command))
        if hasattr(mod, 'setup'):
            getattr(mod, 'setup')(subparsers)

    if len(sys.argv) == 1:
        # Handle the case where no arguments or options are passed
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    # If a subcommand was requested, call the appropriate subcommand's
    # main method
    sys.exit(args.func(args))
