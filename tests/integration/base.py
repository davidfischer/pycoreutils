import os.path
import subprocess
import sys
import unittest


PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
os.environ['PYTHONPATH'] = PROJECT_PATH


class BaseIntegrationTest(unittest.TestCase):
    base_path = PROJECT_PATH

    def _call_pycoreutils(self, args, stdin=None):
        # Call PyCoreutils with "args" and return the status code,
        #  stdout and stderr

        command_path = os.path.join(self.base_path, 'scripts', 'pycoreutils')
        p = subprocess.Popen(['python', command_path] + args, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()

        return p.returncode, stdout, stderr
