from __future__ import unicode_literals

import argparse
import unittest

from pycoreutils.commands._basename import Command


class TestBase64(unittest.TestCase):
    def setUp(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        self.command = Command(subparsers)

    def test_get_base_name(self):
        pairs = (
            ('/path/to/file.c', 'file.c', ''),
            ('/path/to/file.c', 'file', '.c'),
            ('', '', '.c'),
        )
        for name, expected, suffix in pairs:
            self.assertEqual(self.command.get_base_name(name, suffix), expected)


if __name__ == '__main__':
    unittest.main()
