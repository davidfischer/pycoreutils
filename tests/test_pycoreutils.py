from __future__ import unicode_literals

import unittest
import pycoreutils

from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_getcommand(self):
        for cmd in pycoreutils.command.__all__:
            pycoreutils.getcommand(cmd[4:])


if __name__ == '__main__':
    unittest.main()
