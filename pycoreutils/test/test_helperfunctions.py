#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import unicode_literals

import fileinput
import unittest

import pycoreutils
from pycoreutils.test import BaseTestCase


class TestCase(BaseTestCase):
    def test_parsefilelist(self):
        self.createfile('foo', size=999, fill='X')
        self.createfile('bar', size=100, fill='\n')
        l = ''
        for line, filename in pycoreutils.parsefilelist(['foo']):
            self.assertEqual(filename, 'foo')
            l += line
        for line, filename in pycoreutils.parsefilelist(['bar']):
            self.assertEqual(filename, 'bar')
            l += line
        self.assertEqual(l, 'X' * 999 + '\n' * 100)

    def test_mode2string(self):
        self.assertEqual(pycoreutils.mode2string(33261), '-rwxr-xr-x')

    def test_runcommandline(self):
        self.assertEqual(self.runcommandline('basename foo')[0], 'foo\n')

    def test_showbanner(self):
        self.assertEqual(pycoreutils.showbanner(width=70),
"  ____  _  _  ___  _____  ____  ____  __  __  ____  ____  __    ___   \n" +\
" (  _ \( \/ )/ __)(  _  )(  _ \( ___)(  )(  )(_  _)(_  _)(  )  / __)  \n" +\
"  )___/ \  /( (__  )(_)(  )   / )__)  )(__)(   )(   _)(_  )(__ \__ \  \n" +\
" (__)   (__) \___)(_____)(_)\_)(____)(______) (__) (____)(____)(___/  \n\n" +\
"-= PyCoreutils version {0} =-".format(pycoreutils.__version__).center(70) +\
"\n")


if __name__ == '__main__':
    unittest.main()
