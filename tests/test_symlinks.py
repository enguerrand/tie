from unittest import TestCase

from tie import symlinks
from tie import cli
import os

from tie.symlinks import NotASymlinkError

FOOBAR_TXT = "../res/foobar.txt"
LINK_FOOBAR = "../res/link_foobar.txt"
FOOBAR_DIR = "../res/foobar.d"
LINK_FOOBAR_DIR = "../res/link_foobar.d"


class TestSymlinks(TestCase):

    def test_readlink(self):
        self._create_test_link()
        dst = symlinks.readlink(LINK_FOOBAR)
        self.assertEqual(dst, FOOBAR_TXT)
        self._remove_test_link()

    def test_ln(self):
        self._remove_test_link()
        symlinks.ln(FOOBAR_TXT, LINK_FOOBAR)
        dst = symlinks.readlink(LINK_FOOBAR)
        self.assertEqual(dst, FOOBAR_TXT)
        self._remove_test_link()

    def test_rmlink(self):
        self._create_test_link()
        symlinks.rm(LINK_FOOBAR)
        self.assertFalse(self._file_exists(LINK_FOOBAR))

    def test_rmfile(self):
        self.assertRaises(NotASymlinkError, lambda: symlinks.rm(FOOBAR_TXT))
        self.assertTrue(self._file_exists(FOOBAR_TXT))

    def test_rmdir(self):
        self._create_test_link_to_dir()
        symlinks.rm(LINK_FOOBAR_DIR)
        self.assertTrue(self._file_exists(FOOBAR_DIR))
        self.assertFalse(self._file_exists(LINK_FOOBAR_DIR))

    def test_rmdir_with_trailing_slash(self):
        self._create_test_link_to_dir()
        symlinks.rm(LINK_FOOBAR_DIR+"/")
        self.assertTrue(self._file_exists(FOOBAR_DIR))
        self.assertFalse(self._file_exists(LINK_FOOBAR_DIR))

    def test_rmdir_with_trailing_slashes(self):
        self._create_test_link_to_dir()
        symlinks.rm(LINK_FOOBAR_DIR+"//")
        self.assertTrue(self._file_exists(FOOBAR_DIR))
        self.assertFalse(self._file_exists(LINK_FOOBAR_DIR))

    def _file_exists(self, path: str) -> bool:
        return os.path.exists(path)

    def _create_test_link(self):
        cli.run_cmd(["ln", "-sf", FOOBAR_TXT, LINK_FOOBAR])

    def _remove_test_link(self):
        cli.run_cmd(["rm", "-f", LINK_FOOBAR])

    def _create_test_link_to_dir(self):
        cli.run_cmd(["mkdir", "-p", FOOBAR_DIR])
        cli.run_cmd(["ln", "-sf", FOOBAR_DIR, LINK_FOOBAR_DIR])
