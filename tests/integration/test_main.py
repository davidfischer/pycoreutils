import sys

from .base import BaseIntegrationTest


class TestMain(BaseIntegrationTest):
    def test_noargs(self):
        status, stdout, stderr = self._call_pycoreutils([])
        self.assertEqual(stderr, b'')
        self.assertEqual(status, 0)

    def test_version(self):
        # Based on changes in argparse
        # the version goes to stdout in 3.4+ and stderr in 2.x and 3.3
        status, stdout, stderr = self._call_pycoreutils(['--version'])
        if sys.version_info < (3, 4):
            self.assertTrue(stderr.startswith(b'pycoreutils v'), stderr)
        else:
            self.assertTrue(stdout.startswith(b'pycoreutils v'), stdout)
        self.assertEqual(status, 0)
