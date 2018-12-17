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

    def tearDown(self):
        self._remove_index()

    def test_initialization(self):
        self.assertTrue(self._file_exists(TEST_INDEX_LOCATION))
        self.assertTrue(self._file_exists(os.path.join(TEST_INDEX_LOCATION, "tags")))

    def test_update_file(self):
        self.index.update("../res/read_md.jpg")
        self.assertTrue(self._file_exists(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_1)))
        self.assertTrue(self._file_exists(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_2)))


    def _remove_index(self):
        cli.run_cmd(["rm", "-rf", TEST_INDEX_LOCATION])

    def _file_exists(self, path: str) -> bool:
        return os.path.exists(path)
