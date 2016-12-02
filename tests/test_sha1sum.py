from __future__ import unicode_literals

from .base import PycoreutilsBaseTest


class TestSha1Sum(PycoreutilsBaseTest):
    def test_sha1_stdin(self):
        result = self.runner.invoke(self.cli, ['sha1sum', '-'], input=b'test')
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3  -\n')

    def test_sha1_file(self):
        with self.runner.isolated_filesystem():
            with open('hello.txt', 'w') as f:
                f.write('test')

            result = self.runner.invoke(self.cli, ['sha1sum', 'hello.txt'])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.output, 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3  hello.txt\n')

    def test_sha1_bsd(self):
        with self.runner.isolated_filesystem():
            with open('hello.txt', 'w') as f:
                f.write('test')

            result = self.runner.invoke(self.cli, ['sha1sum', '--tag', 'hello.txt'])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.output, 'SHA1 (hello.txt) = a94a8fe5ccb19ba61c4c0873d391e987982fbbd3\n')

    def test_sha1_invalid_options(self):
        result = self.runner.invoke(self.cli, ['sha1sum', '--tag', '--check', '-'], input=b'')
        self.assertTrue(result.exit_code != 0)

        result = self.runner.invoke(self.cli, ['sha1sum', '--status', '-'], input=b'')
        self.assertTrue(result.exit_code != 0)

        result = self.runner.invoke(self.cli, ['sha1sum', '--quiet', '-'], input=b'')
        self.assertTrue(result.exit_code != 0)

    def test_sha1_check(self):
        expected_checksums = (
            'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3  hello.txt\n'
            'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3  hello2.txt\n'
        )

        with self.runner.isolated_filesystem():
            with open('hello.txt', 'w') as f:
                f.write('test')

            with open('hello2.txt', 'w') as f:
                f.write('test')

            result = self.runner.invoke(self.cli, ['sha1sum', 'hello.txt', 'hello2.txt'])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.output, expected_checksums)

            with open('checksum.txt', 'w') as f:
                f.write(result.output)

            result = self.runner.invoke(self.cli, ['sha1sum', '--check', 'checksum.txt'])
            self.assertEqual(result.exit_code, 0)

            result = self.runner.invoke(self.cli, ['sha1sum', '--check', '--quiet', 'checksum.txt'])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.output, '')

            result = self.runner.invoke(self.cli, ['sha1sum', '--check', '--status', 'checksum.txt'])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.output, '')

    def test_sha1_check_fail(self):
        checksums = (
            'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3  hello.txt\n'
            'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3  hello2.txt\n'
        )

        with self.runner.isolated_filesystem():
            with open('hello.txt', 'w') as f:
                f.write('test')

            with open('hello2.txt', 'w') as f:
                f.write('testtest')

            with open('checksum.txt', 'w') as f:
                f.write(checksums)

            result = self.runner.invoke(self.cli, ['sha1sum', '--check', 'checksum.txt'])
            self.assertTrue(result.exit_code != 0)
            self.assertTrue('hello2.txt: FAILED' in result.output)
            self.assertTrue('WARNING: 1 computed checksum did NOT match' in result.output)
