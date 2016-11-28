from __future__ import unicode_literals

from .base import PycoreutilsBaseTest


class TestMain(PycoreutilsBaseTest):
    def test_noargs(self):
        result = self.runner.invoke(self.cli, [])
        self.assertEqual(result.exit_code, 0)

    def test_version(self):
        result = self.runner.invoke(self.cli, ['--version'])
        self.assertEqual(result.exit_code, 0)
        # The executable name will be pycoreutils after deploying
        self.assertTrue(result.output.startswith('cli v'), result.output)

    def test_invalid_command(self):
        result = self.runner.invoke(self.cli, ['invalidsubcommand'])
        self.assertEqual(result.exit_code, 2)
        self.assertTrue('Error: No such command' in result.output, result.output)
