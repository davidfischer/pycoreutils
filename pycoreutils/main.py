import importlib

from .commands import commands
from .vendor import click
from .version import __version__


class PycoreutilsMulticommand(click.MultiCommand):
    def list_commands(self, ctx):
        return commands

    def get_command(self, ctx, name):
        try:
            mod = importlib.import_module(u'pycoreutils.commands._{}'.format(name))
            if hasattr(mod, 'subcommand'):
                return getattr(mod, 'subcommand')
        except ImportError:
            pass

        return None


@click.command(
    cls=PycoreutilsMulticommand,
    epilog='See "COMMAND -h" to read about a specific subcommand',
    short_help='%(prog)s [-h] COMMAND [args]',
)
@click.help_option('-h', '--help')
@click.version_option(__version__, '-v', '--version', message='%(prog)s v%(version)s')
def cli():
    '''
    Coreutils in Pure Python

    \b
     ____  _  _  ___  _____  ____  ____  __  __  ____  ____  __    ___
    (  _ \( \/ )/ __)(  _  )(  _ \( ___)(  )(  )(_  _)(_  _)(  )  / __)
     )___/ \  /( (__  )(_)(  )   / )__)  )(__)(   )(   _)(_  )(__ \__ \\
    (__)   (__) \___)(_____)(_)\_)(____)(______) (__) (____)(____)(___/
    '''
    pass
