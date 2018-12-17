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
        self.files_base_path = os.path.abspath("../res").replace(os.sep, ":")

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

    def _remove_index(self):
        cli.run_cmd(["rm", "-rf", TEST_INDEX_LOCATION])

    def _file_exists(self, path: str) -> bool:
        return os.path.exists(path)
