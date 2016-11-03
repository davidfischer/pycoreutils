from __future__ import unicode_literals

import os
import stat
import time
import unittest

from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_ls(self):
        self.setup_filesystem()
        self.assertEqual(
            self.runcommandline('ls')[0],
            'dir1\ndir2\nfile1\nfile2.txt\nfile3.empty\n'
        )

    def test_ls_l(self):
        os.mkdir('biz')
        self.createfile('foo', size=100)
        self.createfile('bar', size=999999)
        os.chmod('bar',
                    stat.S_IWUSR +\
                    stat.S_IRGRP +\
                    stat.S_IWOTH +\
                    stat.S_IXOTH
        )

        uid = os.getuid()
        gid = os.getgid()
        date = time.strftime('%Y-%m-%d %H:%m', time.localtime())
        self.assertEqual(
            self.runcommandline('ls -l')[0],
        '--w-r---wx 1 {0:<5} {1:<5} 999999 {2} bar\n'.format(uid, gid, date) +\
        'drwxr-xr-x 2 {0:<5} {1:<5}     40 {2} biz\n'.format(uid, gid, date) +\
        '-rw-r--r-- 1 {0:<5} {1:<5}    100 {2} foo\n'.format(uid, gid, date)
        )

if __name__ == '__main__':
    unittest.main()
