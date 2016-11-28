import os

from ...vendor import click


@click.command(
    help='Print NAME with any leading directory components removed.',
    short_help='Remove leading directory from names',
)
@click.help_option('-h', '--help')
@click.option('-a', '--multiple', is_flag=True, help='For compatibility only')
@click.option('-z', '--zero', is_flag=True, default=False, help='end each output line with NUL, not newline')
@click.option('-s', '--suffix', metavar='SUFFIX', help='remove a trailing SUFFIX as well')
@click.option('--separator', metavar='SEPARATOR', help='the directory separator [default: "{}"]'.format(os.sep), default=os.sep)
@click.argument('names', metavar='NAME', nargs=-1)
def subcommand(multiple, zero, suffix, separator, names):
    # This command differs from its GNU alternative in that -a is always assumed
    # --separator is non-standard as well but handy on Windows especially
    line_ending = '\n'
    if zero:
        line_ending = '\0'

    for n in names:
        click.echo(u'{}{}'.format(get_base_name(n, suffix, separator), line_ending), nl=False)


def get_base_name(name, suffix, separator):
    base_name = name.split(separator)[-1]
    if suffix and base_name.endswith(suffix):
        base_name = base_name[:-len(suffix)]

    return base_name
