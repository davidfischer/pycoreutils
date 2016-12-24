from __future__ import unicode_literals

from .base import PycoreutilsBaseTest


class TestTee(PycoreutilsBaseTest):
    def test_tee(self):
        result = self.runner.invoke(self.cli, ['tee'], input=b'test')
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'test')
