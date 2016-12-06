from __future__ import unicode_literals

from .base import PycoreutilsBaseTest


class TestSha512Sum(PycoreutilsBaseTest):
    """
    Very little code is unique to the sha512sum command
    Instead most of the actual tests are in `test_sha1sum.py`
    """

    def test_sha512_stdin(self):
        result = self.runner.invoke(self.cli, ['sha512sum', '-'], input=b'test')
        expected = 'ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff  -\n'
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, expected)
