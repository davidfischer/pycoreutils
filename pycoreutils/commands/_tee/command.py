import functools

from ...vendor import click


@click.command(
    help='Copy standard input to each FILE and to standard output.',
)
@click.help_option('-h', '--help')
@click.option('-a', '--append', is_flag=True, default=False, help='append to the given FILEs, do not overwrite')
@click.argument('files', metavar='FILE', required=False, nargs=-1, type=click.Path())
def subcommand(append, files):
    stdin = click.get_binary_stream('stdin')

    if append:
        mode = 'ab'
    else:
        mode = 'wb'

    fds = [open(click.format_filename(f), mode) for f in files]

    for data in iter(functools.partial(stdin.read, 4096), b''):
        for fd in fds:
            fd.write(data)
        click.echo(data, nl=False)
