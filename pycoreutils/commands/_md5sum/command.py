import sys

from ..hasher import HasherCommand
from ...vendor import click


@click.command(
    help='Print or check MD5 checksums',
)
@click.help_option('-h', '--help')
@click.option('-c', '--check', is_flag=True, default=False, help='read MD5 sums from the FILEs and check them')
@click.option('--tag', is_flag=True, default=False, help='Output a BSD-style checksum file')
@click.option('--quiet', is_flag=True, default=False, help="don't print OK for each successfully verified file")
@click.option('--status', is_flag=True, default=False, help="don't output anything, status code shows success")
@click.argument('files', metavar='FILE', required=False, nargs=-1, type=click.File('rb'))
def subcommand(check, tag, quiet, status, files):
    if len(files) == 0:
        files = (click.get_binary_stream('stdin'),)

    hasher = HasherCommand('md5', tag, quiet, status)
    success = hasher.process_files(files, check)

    if not success:
        sys.exit(1)
