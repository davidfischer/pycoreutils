import functools
import hashlib
import re

from ..vendor import click


class HasherCommand(object):
    def __init__(self, algorithm, tag=False, quiet=False, status=False):
        """
        :param algorithm: the hashing algorithm to use (eg. 'sha1', 'md5')
        """
        self.algorithm = algorithm
        self.tag = tag
        self.quiet = quiet
        self.status = status

        hashlen = len(hashlib.new(algorithm).hexdigest())
        self.checksum_line_regex = re.compile('^(?P<checksum>[a-f0-9]{{{hashlen}}})  (?P<filepath>.+)$'.format(hashlen=hashlen).encode('ascii'))

    def process_files(self, files, check=False):
        success = True

        if check and self.tag:
            raise click.BadOptionUsage('the --tag option is meaningless when verifying checksums')

        if not check and (self.status or self.quiet):
            raise click.BadOptionUsage('--status is only meaningful when verifying checksums')

        for file in files:
            if not check:
                # in testing, BytesIO has not attribute "name"
                filepath = getattr(file, 'name', '-')
                checksum = self.checksum_calculator(file)
                if self.tag:
                    click.echo('{} ({}) = {}'.format(self.algorithm.upper(), filepath, checksum))
                else:
                    click.echo('{}  {}'.format(checksum, filepath))
            else:
                success = self.checksum_verifier(file) and success

        return success

    def checksum_calculator(self, file):
        """
        Computes a checksum using the class' algorithm
        Returns a unicode of the hexdigest

        Assumes the file is opened in binary mode
        """
        h = hashlib.new(self.algorithm)
        for data in iter(functools.partial(file.read, 4096), b''):
            h.update(data)
        return h.hexdigest()

    def checksum_verifier(self, file):
        noformat_count = 0
        nomatch_count = 0
        noread_count = 0

        for line in file:
            match = self.checksum_line_regex.match(line)
            if not match:
                noformat_count += 1
            else:
                group = match.groupdict()
                checksum = group['checksum']
                filepath = click.format_filename(group['filepath'])
                try:
                    with click.open_file(filepath, 'rb') as fd:
                        calculated_checksum = self.checksum_calculator(fd).encode('ascii')
                except IOError:
                    noread_count += 1
                    if not self.status:
                        click.echo('{}: FAILED open or read'.format(filepath))
                    continue

                if checksum == calculated_checksum:
                    output = 'OK'
                else:
                    output = 'FAILED'
                    nomatch_count += 1

                if not self.status:
                    if not self.quiet or output != 'OK':
                        click.echo('{}: {}'.format(filepath, output))

        if not self.status:
            if noformat_count == 1:
                click.echo('WARNING: 1 line is improperly formatted', err=True)
            if noformat_count > 1:
                click.echo('WARNING: {} lines are improperly formatted'.format(noformat_count), err=True)
            if noread_count == 1:
                click.echo('WARNING: 1 listed file could not be read', err=True)
            if noread_count > 1:
                click.echo('WARNING: {} listed files could not be read'.format(noread_count), err=True)
            if nomatch_count == 1:
                click.echo('WARNING: 1 computed checksum did NOT match', err=True)
            if nomatch_count > 1:
                click.echo('WARNING: {} computed checksum did NOT match'.format(nomatch_count), err=True)

        return noformat_count + nomatch_count + noread_count == 0
