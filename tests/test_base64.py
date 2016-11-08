from __future__ import unicode_literals

import io
import sys
import unittest

from pycoreutils.command._base64 import encode, decode


class TestBase64(unittest.TestCase):
    def setUp(self):
        sys.stdout = io.BytesIO()

    def test_base64_decode(self):
        return_code = decode(io.BytesIO(b'SGF2ZSBhIGxvdCBvZiBmdW4uLi4K'))
        self.assertEqual(return_code, 0)
        self.assertEqual(sys.stdout.getvalue(), b'Have a lot of fun...\n')

    def test_b64_long_decode(self):
        return_code = decode(io.BytesIO(b'TG9M' * 4096))
        self.assertEqual(return_code, 0)
        self.assertEqual(sys.stdout.getvalue(), b'LoL' * 4096)

    def test_base64_encode(self):
        return_code = encode(io.BytesIO(b'Have a lot of fun...\n'), wrap=5)
        self.assertEqual(return_code, 0)
        self.assertEqual(sys.stdout.getvalue(), b'SGF2Z\nSBhIG\nxvdCB\nvZiBm\ndW4uL\ni4K\n')

    def test_base64_long_encode(self):
        return_code = encode(io.BytesIO(b'LoL' * 4096), wrap=0)
        self.assertEqual(return_code, 0)
        self.assertEqual(sys.stdout.getvalue(), b'TG9M' * 4096)

    def test_invalid_b64(self):
        return_code = decode(io.BytesIO(b'*234'))
        self.assertEqual(return_code, 1)


if __name__ == '__main__':
    unittest.main()
