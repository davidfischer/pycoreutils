from .base import BaseIntegrationTest
from pycoreutils.vendor import six


class TestMain(BaseIntegrationTest):
    def test_noargs(self):
        status, stdout, stderr = self._call_pycoreutils([])
        self.assertEqual(stderr, b'')
        self.assertEqual(status, 0)

    def test_version(self):
        # Based on changes in argparse between 2.x and 3.x
        # the version goes to stdout in 3.x and stderr in 2.x
        status, stdout, stderr = self._call_pycoreutils(['--version'])
        if six.PY2:
            self.assertTrue(stderr.startswith(b'pycoreutils v'), stderr)
        elif six.PY3:
            self.assertTrue(stdout.startswith(b'pycoreutils v'), stdout)
        self.assertEqual(status, 0)
