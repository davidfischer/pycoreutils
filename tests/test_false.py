from __future__ import unicode_literals

from .base import PycoreutilsBaseTest


class TestFalse(PycoreutilsBaseTest):
    def test_false(self):
        result = self.runner.invoke(self.cli, ['false'])
        self.assertEqual(result.exit_code, 1)
