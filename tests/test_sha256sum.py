from __future__ import unicode_literals

from .base import PycoreutilsBaseTest


class TestSha256Sum(PycoreutilsBaseTest):
    """
    Very little code is unique to the sha256sum command
    Instead most of the actual tests are in `test_sha1sum.py`
    """

    def test_sha256_stdin(self):
        result = self.runner.invoke(self.cli, ['sha256sum', '-'], input=b'test')
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08  -\n')
