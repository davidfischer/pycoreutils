from __future__ import unicode_literals

from .base import PycoreutilsBaseTest


class TestTrue(PycoreutilsBaseTest):
    def test_true(self):
        result = self.runner.invoke(self.cli, ['true'])
        self.assertEqual(result.exit_code, 0)
