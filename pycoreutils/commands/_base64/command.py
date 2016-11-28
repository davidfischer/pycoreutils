import base64
import binascii
import functools
import re
import sys
import textwrap

from ...vendor import click


COMMAND_NAME = 'base64'

# Because every 3 bytes map to 4 base64 bytes, the buffer should be
#  a multiple of 3. Conveniently, this is also a multiple of 4 for decoding
BUFSIZE = 3 * 1024


@click.command(
    help='Base64 encode or decode FILE or standard input, to standard output',
    short_help='Base64 encode or decode input',
)
@click.help_option('-h', '--help')
@click.option('-d', '--decode', is_flag=True, default=False, help='decode data')
@click.option('-w', '--wrap', metavar='COLS', default=76, help='wrap encoded lines after COLS character (default %(default)s). Use 0 to disable line wrapping')
@click.argument('file', metavar='FILE', required=False, nargs=1, type=click.File('rb'))
def subcommand(decode, wrap, file):
    if not file:
        file = click.get_binary_stream('stdin')

    if decode:
        decode_base64(file)
    else:
        encode_base64(file, wrap)


def _validated_b64decode(b64_buffer):
    # Ensures the base64_buffer is valid b64
    if sys.version_info >= (3, 0):
        return base64.b64decode(b64_buffer, validate=True)
    else:
        if not re.match(b'^[A-Za-z0-9+/]*={0,2}$', b64_buffer):
            raise binascii.Error('Non-base64 digit found')
        return base64.b64decode(b64_buffer)


def decode_base64(fd):
    """
    Base64 decode the contents of a file
    """
    inputbuffer = b''

    for chunk in iter(functools.partial(fd.read, BUFSIZE), b''):
        inputbuffer += chunk.replace(b'\n', b'')

        while len(inputbuffer) > BUFSIZE:
            # Ensure we output a multiple of BUFSIZE b64 bytes
            b64_to_output = inputbuffer[:BUFSIZE]
            inputbuffer = inputbuffer[BUFSIZE:]

            # Validate the base64 bytes, convert them to binary
            # and output them
            try:
                click.echo(_validated_b64decode(b64_to_output), nl=False)
            except (binascii.Error, TypeError):
                click.echo('{}: invalid input'.format(COMMAND_NAME), err=True)
                sys.exit(1)

    if len(inputbuffer) > 0:
        # output any remaining bytes
        try:
            click.echo(_validated_b64decode(inputbuffer), nl=False)
        except (binascii.Error, TypeError):
            click.echo('{}: invalid input'.format(COMMAND_NAME), err=True)
            sys.exit(1)


def encode_base64(fd, wrap):
    """
    Base64 encode the contents of a file

    Wrap the results based on `wrap` number of columns
    """
    outputbuffer = b''

    for chunk in iter(functools.partial(fd.read, BUFSIZE), b''):
        outputbuffer += base64.b64encode(chunk)

        if wrap <= 0:
            click.echo(outputbuffer, nl=False)
            outputbuffer = b''
        else:
            # Use as many bytes from the outputbuffer as possible while maintaining
            # that it is a multiple of `wrap`.
            num_bytes = wrap * int(len(outputbuffer) / wrap)
            text = outputbuffer[:num_bytes].decode('ascii')
            outputbuffer = outputbuffer[num_bytes:]

            # Wrap the results based on `wrap`
            for line in textwrap.wrap(text, width=wrap):
                click.echo(line.encode('ascii'))

    if len(outputbuffer) > 0:
        # print any remaining bytes
        click.echo(outputbuffer)
