import os
from unittest import TestCase

import lib.exif_editor as ee
from lib import cli
from lib.index import Index
from tests.test_defines import *

TEST_INDEX_LOCATION = "../res/index"


class TestIndex(TestCase):

    def setUp(self):
        _remove_index()
        self.index = Index(TEST_INDEX_LOCATION, ee.ExifEditor("Exif.Photo.UserComment"))
        self.files_base_path = _path_to_linkname(os.path.abspath("../res"))

    def tearDown(self):
        _remove_index()

    def test_initialization(self):
        self.assertTrue(os.path.isdir(TEST_INDEX_LOCATION))
        self.assertTrue(os.path.isdir(os.path.join(TEST_INDEX_LOCATION, "tags")))

    def test_update_file(self):
        self.index.update("../res/read_md.jpg")
        link_name = self.files_base_path + ":" + "read_md.jpg"
        self.assertTrue(os.path.islink(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_1.lower(), link_name)),
                        "no link in tagdir 1")
        self.assertTrue(os.path.islink(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_2.lower(), link_name)),
                        "no link in tagdir 2")

    def test_list_tags(self):
        cli.run_cmd(["mkdir", "-p", os.path.join(TEST_INDEX_LOCATION, "tags", "foo")])
        cli.run_cmd(["mkdir", "-p", os.path.join(TEST_INDEX_LOCATION, "tags", "bar")])
        tags = self.index.list_tags()
        self.assertEqual(["foo", "bar"], tags, "tags list incorrect")

    def test_list_files(self):
        self.index.update(READ_FILE_MD)
        files = self.index.list_files(TEST_READ_TAG_1)
        self.assertEqual([os.path.abspath(READ_FILE_MD)], files, "files list incorrect")

    def test_update_file_invalid_md(self):
        img = os.path.abspath("../res/read.jpg")
        linkname = _path_to_linkname(img)
        removed_tag_dir = os.path.join(TEST_INDEX_LOCATION, "tags", "removed tag")
        link_path = os.path.join(removed_tag_dir, linkname)
        cli.run_cmd(["mkdir", "-p", removed_tag_dir])
        cli.run_cmd(["ln", "-sf", img, link_path])
        self.index.update("../res/read.jpg")
        self.assertFalse(os.path.islink(link_path), "tag was not removed!")

    def test_update_vanished_file(self):
        vanished_file = "../res/vanished_file.jpg"
        link_path = self._prepare_vanished_file(vanished_file, TEST_READ_TAG_2)
        self.index.update(vanished_file)
        self.assertFalse(os.path.islink(link_path), "tag of vanished file was not removed!")

    def test_list_vanished_file(self):
        vanished_file = "../res/vanished_file.jpg"
        link_path = self._prepare_vanished_file(vanished_file, TEST_READ_TAG_2)
        self.index.list_files(TEST_READ_TAG_2)
        self.assertFalse(os.path.islink(link_path), "tag of vanished file was not removed!")

    def test_update_vanished_directory(self):
        vanished_directory = "../res/vanished_directory"
        vanished_file = os.path.join(vanished_directory, "some_subdir/vanished_file.jpg")
        link_path = self._prepare_vanished_file(vanished_file, TEST_READ_TAG_2)
        self.index.update(vanished_directory)
        self.assertFalse(os.path.islink(link_path), "tag of file in vanished directory was not removed!")

    def test_list_vanished_directory(self):
        vanished_directory = "../res/vanished_directory"
        vanished_file = os.path.join(vanished_directory, "some_subdir/vanished_file.jpg")
        link_path = self._prepare_vanished_file(vanished_file, TEST_READ_TAG_2)
        self.index.list_files(TEST_READ_TAG_2)
        self.assertFalse(os.path.islink(link_path), "tag of file in vanished directory was not removed!")

    def _prepare_vanished_file(self, path: str, tag_name: str) -> str:
        img = os.path.abspath(path)
        linkname = _path_to_linkname(img)
        tag_dir = os.path.join(TEST_INDEX_LOCATION, "tags", tag_name)
        link_path = os.path.join(tag_dir, linkname)
        cli.run_cmd(["mkdir", "-p", tag_dir])
        cli.run_cmd(["ln", "-sf", img, link_path])
        return link_path

    def test_update_dir(self):
        self.index.update("../res/recursive.d")
        link_name_root = self.files_base_path + ":recursive.d:" + "read_md.jpg"
        link_name_lvl1 = self.files_base_path + ":recursive.d:level1:" + "read_md.jpg"
        link_name_lvl2 = self.files_base_path + ":recursive.d:level1:level2:" + "read_md.jpg"
        for link_name in [link_name_root, link_name_lvl1, link_name_lvl2]:
            self.assertTrue(os.path.islink(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_1.lower(), link_name)),
                            "Link "+link_name+" should exist in tagdir 1 but does not")
            self.assertTrue(os.path.islink(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_2.lower(), link_name)),
                            "Link "+link_name+" should exist in tagdir 2 but does not")

    def test_removed_tag(self):
        img = os.path.abspath("../res/read_md.jpg")
        linkname = _path_to_linkname(img)
        removed_tag_dir = os.path.join(TEST_INDEX_LOCATION, "tags", "removed tag")
        link_path = os.path.join(removed_tag_dir, linkname)
        cli.run_cmd(["mkdir", "-p", removed_tag_dir])
        cli.run_cmd(["ln", "-sf", img, link_path])
        self.index.update("../res/read_md.jpg")
        self.assertFalse(os.path.islink(link_path), "tag was not removed!")
        # Execute again to test if this (incorrectly) raises a FileNotFoundError
        self.index.update("../res/read_md.jpg")

    def test_auto_remove_empty_tag_dir(self):
        empty_tag_dir = os.path.join(TEST_INDEX_LOCATION, "tags", "removed tag")
        cli.run_cmd(["mkdir", "-p", empty_tag_dir])
        self.index.update("../res/read_md.jpg")
        self.assertFalse(os.path.isdir(empty_tag_dir), "empty tag dir was not removed!")


def _path_to_linkname(img):
    return img.replace(os.sep, ":")


def _remove_index():
    cli.run_cmd(["rm", "-rf", TEST_INDEX_LOCATION])
