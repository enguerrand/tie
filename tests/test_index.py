import os
from unittest import TestCase

import pytag.exif_editor as ee
from pytag import cli
from pytag.index import Index
from tests.test_tags import *

TEST_INDEX_LOCATION = "../res/index"


class TestIndex(TestCase):

    def setUp(self):
        self._remove_index()
        self.index = Index(TEST_INDEX_LOCATION, ee.ExifEditor())
        self.files_base_path = self._path_to_linkname(os.path.abspath("../res"))

    def tearDown(self):
        self._remove_index()

    def test_initialization(self):
        self.assertTrue(self._file_exists(TEST_INDEX_LOCATION))
        self.assertTrue(self._file_exists(os.path.join(TEST_INDEX_LOCATION, "tags")))

    def test_update_file(self):
        self.index.update("../res/read_md.jpg")
        link_name = self.files_base_path + ":" + "read_md.jpg"
        self.assertTrue(self._file_exists(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_1, link_name)),
                        "no link in tagdir 1")
        self.assertTrue(self._file_exists(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_2, link_name)),
                        "no link in tagdir 2")

    def test_update_file_invalid_md(self):
        img = os.path.abspath("../res/read.jpg")
        linkname = self._path_to_linkname(img)
        removed_tag_dir = os.path.join(TEST_INDEX_LOCATION, "tags", "removed tag")
        link_path = os.path.join(removed_tag_dir, linkname)
        cli.run_cmd(["mkdir", "-p", removed_tag_dir])
        cli.run_cmd(["ln", "-sf", img, link_path])
        self.index.update("../res/read.jpg")
        self.assertFalse(self._file_exists(link_path), "tag was not removed!")
        cli.run_cmd(["rm", "-rf", removed_tag_dir])

    def test_update_vanished_file(self):
        img = os.path.abspath("../res/vanished_file.jpg")
        linkname = self._path_to_linkname(img)
        tag_dir = os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_2)
        link_path = os.path.join(tag_dir, linkname)
        cli.run_cmd(["mkdir", "-p", tag_dir])
        cli.run_cmd(["ln", "-sf", img, link_path])
        self.index.update("../res/vanished_file.jpg")
        self.assertFalse(self._file_exists(link_path), "tag of vanished file was not removed!")
        cli.run_cmd(["rm", "-rf", tag_dir])

    def test_update_dir(self):
        self.index.update("../res/recursive.d")
        link_name_root = self.files_base_path + ":recursive.d:" + "read_md.jpg"
        link_name_lvl1 = self.files_base_path + ":recursive.d:level1:" + "read_md.jpg"
        link_name_lvl2 = self.files_base_path + ":recursive.d:level1:level2:" + "read_md.jpg"
        for link_name in [link_name_root, link_name_lvl1, link_name_lvl2]:
            self.assertTrue(self._file_exists(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_1, link_name)),
                            "Link "+link_name+" should exist in tagdir 1 but does not")
            self.assertTrue(self._file_exists(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_2, link_name)),
                            "Link "+link_name+" should exist in tagdir 2 but does not")

    def test_removed_tag(self):
        img = os.path.abspath("../res/read_md.jpg")
        linkname = self._path_to_linkname(img)
        removed_tag_dir = os.path.join(TEST_INDEX_LOCATION, "tags", "removed tag")
        link_path = os.path.join(removed_tag_dir, linkname)
        cli.run_cmd(["mkdir", "-p", removed_tag_dir])
        cli.run_cmd(["ln", "-sf", img, link_path])
        self.index.update("../res/read_md.jpg")
        self.assertFalse(self._file_exists(link_path), "tag was not removed!")
        # Execute again to test if this (incorrectly) raises a FileNotFoundError
        self.index.update("../res/read_md.jpg")
        cli.run_cmd(["rm", "-rf", removed_tag_dir])

    def _path_to_linkname(self, img):
        return img.replace(os.sep, ":")

    def _remove_index(self):
        cli.run_cmd(["rm", "-rf", TEST_INDEX_LOCATION])

    def _file_exists(self, path: str) -> bool:
        return os.path.exists(path)
