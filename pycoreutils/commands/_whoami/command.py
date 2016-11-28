import getpass

from ...vendor import click


@click.command(
    help='Print the username of the current user',
    short_help='Print the current user',
)
@click.help_option('-h', '--help')
def subcommand():
    click.echo(getpass.getuser())
