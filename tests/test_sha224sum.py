from __future__ import unicode_literals

from .base import PycoreutilsBaseTest


class TestSha224Sum(PycoreutilsBaseTest):
    """
    Very little code is unique to the sha224sum command
    Instead most of the actual tests are in `test_sha1sum.py`
    """

    def test_224_stdin(self):
        result = self.runner.invoke(self.cli, ['sha224sum', '-'], input=b'test')
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, '90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809  -\n')
