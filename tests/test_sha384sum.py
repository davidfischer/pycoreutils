from __future__ import unicode_literals

from .base import PycoreutilsBaseTest


class TestSha384Sum(PycoreutilsBaseTest):
    """
    Very little code is unique to the sha384sum command
    Instead most of the actual tests are in `test_sha1sum.py`
    """

    def test_sha384_stdin(self):
        result = self.runner.invoke(self.cli, ['sha384sum', '-'], input=b'test')
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, '768412320f7b0aa5812fce428dc4706b3cae50e02a64caa16a782249bfe8efc4b7ef1ccb126255d196047dfedf17a0a9  -\n')
