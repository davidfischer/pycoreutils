from __future__ import print_function, unicode_literals

import argparse
import base64
import binascii
import functools
import re
import sys
import textwrap

from ..vendor import six


COMMAND_NAME = 'base64'

# Because every 3 bytes map to 4 base64 bytes, the buffer should be
#  a multiple of 3. Conveniently, this is also a multiple of 4 for decoding
BUFSIZE = 3 * 1024


def setup(subparsers):
    p = subparsers.add_parser(
        COMMAND_NAME,
        description='Base64 encode or decode FILE or standard input, to standard output',
        help='Base64 encode or decode input',
        usage='{} [options] [args]'.format(COMMAND_NAME),
    )
    p.add_argument('fd', metavar='FILE', nargs='?', type=argparse.FileType('rb'),
                   default=sys.stdin, help='a file to base64 encode or decode')
    p.add_argument('-d', '--decode', action='store_true', dest='decode', help='decode data')
    p.add_argument('-w', dest='wrap', default=76, type=int,
                   help='wrap encoded lines after COLS character (default %(default)s). '
                        'Use 0 to disable line wrapping')
    p.set_defaults(func=main)


def main(args):
    if args.decode:
        return decode(args.fd)
    else:
        return encode(args.fd, args.wrap)


def _validated_b64decode(b64_buffer):
    # Ensures the base64_buffer is valid b64
    if six.PY3:
        return base64.b64decode(b64_buffer, validate=True)
    else:
        if not re.match(b'^[A-Za-z0-9+/]*={0,2}$', b64_buffer):
            raise binascii.Error('Non-base64 digit found')
        return base64.b64decode(b64_buffer)


def decode(fd):
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
                sys.stdout.write(_validated_b64decode(b64_to_output))
            except (binascii.Error, TypeError):
                sys.stderr.write('{}: invalid input\n'.format(COMMAND_NAME))
                return 1

    if len(inputbuffer) > 0:
        # output any remaining bytes
        try:
            sys.stdout.write(_validated_b64decode(inputbuffer))
        except (binascii.Error, TypeError):
            sys.stderr.write('{}: invalid input\n'.format(COMMAND_NAME))
            return 1

    return 0


def encode(fd, wrap):
    """
    Base64 encode the contents of a file

    Wrap the results based on `wrap` number of columns
    """
    outputbuffer = b''

    for chunk in iter(functools.partial(fd.read, BUFSIZE), b''):
        outputbuffer += base64.b64encode(chunk)

        if wrap <= 0:
            sys.stdout.write(outputbuffer)
            outputbuffer = b''
        else:
            # Use as many bytes from the outputbuffer as possible while maintaining
            # that it is a multiple of `wrap`.
            num_bytes = wrap * int(len(outputbuffer) / wrap)
            text = outputbuffer[:num_bytes].decode('ascii')
            outputbuffer = outputbuffer[num_bytes:]

            # Wrap the results based on `wrap`
            for line in textwrap.wrap(text, width=wrap):
                sys.stdout.write(line.encode('ascii'))
                sys.stdout.write(b'\n')

    if len(outputbuffer) > 0:
        # print any remaining bytes
        sys.stdout.write(outputbuffer)
        sys.stdout.write(b'\n')

    return 0
