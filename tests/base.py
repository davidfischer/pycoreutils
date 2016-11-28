import unittest

from pycoreutils.main import cli
from pycoreutils.vendor.click.testing import CliRunner


class PycoreutilsBaseTest(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.cli = cli
