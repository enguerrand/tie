# -*- coding: utf-8 -*-
from unittest import TestCase

from lib import symlinks
from lib import cli
import os

from lib.symlinks import NotASymlinkError

FOOBAR_TXT = "../res/foobar.txt"
LINK_FOOBAR = "../res/link_foobar.txt"
FOOBAR_DIR = "../res/foobar.d"
LINK_FOOBAR_DIR = "../res/link_foobar.d"


class TestSymlinks(TestCase):

    def test_valid(self):
        _create_test_link()
        self.assertFalse(symlinks.is_broken(LINK_FOOBAR), "link should not be broken")
        _remove_test_link()

    def test_broken(self):
        _create_broken_test_link()
        self.assertTrue(symlinks.is_broken(LINK_FOOBAR), "link should be broken")
        _remove_test_link()

    def test_readlink(self):
        _create_test_link()
        dst = symlinks.readlink(LINK_FOOBAR)
        self.assertEqual(dst, FOOBAR_TXT)
        _remove_test_link()

    def test_ln(self):
        _remove_test_link()
        symlinks.ln(FOOBAR_TXT, LINK_FOOBAR)
        dst = symlinks.readlink(LINK_FOOBAR)
        self.assertEqual(dst, FOOBAR_TXT)
        _remove_test_link()

    def test_ln_broken_on_file(self):
        self.assertTrue(symlinks.is_broken(FOOBAR_TXT))

    def test_rmlink(self):
        _create_test_link()
        symlinks.rm(LINK_FOOBAR)
        self.assertFalse(_file_exists(LINK_FOOBAR))

    def test_rmfile(self):
        self.assertRaises(NotASymlinkError, lambda: symlinks.rm(FOOBAR_TXT))
        self.assertTrue(_file_exists(FOOBAR_TXT))

    def test_rmdir(self):
        _create_test_link_to_dir()
        symlinks.rm(LINK_FOOBAR_DIR)
        self.assertTrue(_file_exists(FOOBAR_DIR))
        self.assertFalse(_file_exists(LINK_FOOBAR_DIR))

    def test_rmdir_with_trailing_slash(self):
        _create_test_link_to_dir()
        symlinks.rm(LINK_FOOBAR_DIR+"/")
        self.assertTrue(_file_exists(FOOBAR_DIR))
        self.assertFalse(_file_exists(LINK_FOOBAR_DIR))

    def test_rmdir_with_trailing_slashes(self):
        _create_test_link_to_dir()
        symlinks.rm(LINK_FOOBAR_DIR+"//")
        self.assertTrue(_file_exists(FOOBAR_DIR))
        self.assertFalse(_file_exists(LINK_FOOBAR_DIR))

        
def _file_exists(path: str) -> bool:
    return os.path.exists(path)


def _create_test_link():
    cli.run_cmd(["ln", "-sf", FOOBAR_TXT, LINK_FOOBAR])


def _create_broken_test_link():
    cli.run_cmd(["ln", "-sf", "/non/existant/file", LINK_FOOBAR])


def _remove_test_link():
    cli.run_cmd(["rm", "-f", LINK_FOOBAR])


def _create_test_link_to_dir():
    cli.run_cmd(["mkdir", "-p", FOOBAR_DIR])
    cli.run_cmd(["ln", "-sf", FOOBAR_DIR, LINK_FOOBAR_DIR])
