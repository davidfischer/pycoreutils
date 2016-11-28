from ...vendor import click


@click.command(
    help='Exit with a successful status code',
)
@click.help_option('-h', '--help')
def subcommand():
    pass
