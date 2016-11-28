from __future__ import unicode_literals

from .base import PycoreutilsBaseTest

from pycoreutils.commands._basename.command import get_base_name


class TestBaseName(PycoreutilsBaseTest):
    def test_get_base_name(self):
        pairs = (
            ('/path/to/file.c', 'file.c', '', '/'),
            ('/path/to/file.c', 'file', '.c', '/'),
            ('', '', '.c', '/'),
            ('c:\\system32\\etc\\hosts.txt', 'hosts.txt', '', '\\'),
        )
        for name, expected, suffix, sep in pairs:
            self.assertEqual(get_base_name(name, suffix, sep), expected)
