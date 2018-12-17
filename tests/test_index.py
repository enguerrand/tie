import os
from unittest import TestCase

from pytag import cli
from pytag.index import Index

TEST_INDEX_LOCATION = "../res/index"


class TestIndex(TestCase):

    def test_initialization(self):
        cli.run_cmd(["rm", "-rf", TEST_INDEX_LOCATION])
        index = Index(TEST_INDEX_LOCATION)
        self.assertTrue(self._file_exists(TEST_INDEX_LOCATION))
        self.assertTrue(self._file_exists(os.path.join(TEST_INDEX_LOCATION, "tags")))

    def _file_exists(self, path: str) -> bool:
        return os.path.exists(path)
