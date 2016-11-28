from __future__ import unicode_literals

import os

from .base import PycoreutilsBaseTest


class TestWhoami(PycoreutilsBaseTest):
    def test_whoami(self):
        test_username = 'pycoreutils-user'
        os.environ['LOGNAME'] = test_username
        result = self.runner.invoke(self.cli, ['whoami'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.strip(), test_username)
