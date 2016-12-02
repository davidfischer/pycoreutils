from __future__ import unicode_literals

from .base import PycoreutilsBaseTest


class TestMd5Sum(PycoreutilsBaseTest):
    """
    Very little code is unique to the md5sum command
    Instead most of the actual tests are in `test_sha1sum.py`
    """

    def test_md5_stdin(self):
        result = self.runner.invoke(self.cli, ['md5sum', '-'], input=b'test')
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, '098f6bcd4621d373cade4e832627b4f6  -\n')
