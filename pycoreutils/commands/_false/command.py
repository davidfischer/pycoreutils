import sys

from ...vendor import click


@click.command(
    help='Exit with a failure status code',
)
@click.help_option('-h', '--help')
def subcommand():
    sys.exit(1)
