from __future__ import unicode_literals

from .base import PycoreutilsBaseTest


class TestBase64(PycoreutilsBaseTest):
    def test_base64_decode(self):
        encoded = b'SGF2ZSBhIGxvdCBvZiBmdW4uLi4K'
        result = self.runner.invoke(self.cli, ['base64', '-d'], input=encoded)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'Have a lot of fun...\n')

    def test_b64_long_decode(self):
        encoded = b'TG9M' * 4096
        result = self.runner.invoke(self.cli, ['base64', '-d'], input=encoded)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'LoL' * 4096)

    def test_base64_encode(self):
        decoded = b'Have a lot of fun...\n'
        result = self.runner.invoke(self.cli, ['base64', '-w5'], input=decoded)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'SGF2Z\nSBhIG\nxvdCB\nvZiBm\ndW4uL\ni4K\n')

    def test_base64_long_encode(self):
        decoded = b'LoL' * 4096
        result = self.runner.invoke(self.cli, ['base64', '-w0'], input=decoded)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'TG9M' * 4096)

    def test_invalid_b64(self):
        encoded = b'*234'
        result = self.runner.invoke(self.cli, ['base64', '-d'], input=encoded)
        self.assertEqual(result.exit_code, 1)
