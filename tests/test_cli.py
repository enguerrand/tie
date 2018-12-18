from subprocess import CalledProcessError
from unittest import TestCase

from pytag import cli


class TestCli(TestCase):
    def test_cat(self):
        lines = cli.run_cmd(["cat", "../res/foobar.txt"])
        self.assertEqual(lines[0], "foo")
        self.assertEqual(lines[1], "bar")

    def test_err(self):
        self.assertRaises(CalledProcessError, lambda: cli.run_cmd(["cat", "../res/fooba.txt"]))
