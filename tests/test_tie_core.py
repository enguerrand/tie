import os
from unittest import TestCase

from tests.test_index import TEST_INDEX_LOCATION
import lib.exif_editor as ee
from lib import cli
from lib import meta_data as md
from lib.index import Index
from lib.meta_data import InvalidMetaDataError
from lib.query import Query, MatchType
from lib.tie_core import TieCore, TieCoreImpl
from tests.defines import *


class TestTieCore(TestCase):
    def setUp(self):
        _remove_index()
        self.exif = ee.ExifEditor("Exif.Photo.UserComment")
        self.files_base_path = _path_to_linkname(os.path.abspath("../res"))
        self.index = Index(TEST_INDEX_LOCATION, self.exif)
        self.tie_core = TieCoreImpl(self.exif, self.index)

    def tearDown(self):
        _remove_index()

    def test_query_all(self):
        self._prepare_query_test()
        files_2_3 = self.tie_core.query(Query([QUERY_TAG_2, QUERY_TAG_3], MatchType.all))
        self.assertEqual([os.path.abspath(QUERY_FILE_2)], files_2_3, "Query all with 2 tags did not find the expected files")
        files_3 = self.tie_core.query(Query([QUERY_TAG_3], MatchType.all))
        self.assertEqual([os.path.abspath(QUERY_FILE_2), os.path.abspath(QUERY_FILE_3)], files_3, "Query all with 1 tag did not find the expected files")
        _clean_after_query_test()

    def test_query_any(self):
        self._prepare_query_test()
        files = self.tie_core.query(Query([QUERY_TAG_2, QUERY_TAG_3], MatchType.any))
        self.assertEqual([os.path.abspath(QUERY_FILE_1), os.path.abspath(QUERY_FILE_2), os.path.abspath(QUERY_FILE_3)], files, "Query any did not find the expected files")
        _clean_after_query_test()

    def _prepare_query_test(self):
        cli.run_cmd(["cp", READ_FILE_MD, QUERY_FILE_1])
        cli.run_cmd(["cp", READ_FILE_MD, QUERY_FILE_2])
        cli.run_cmd(["cp", READ_FILE_MD, QUERY_FILE_3])
        cli.run_cmd(["cp", READ_FILE_MD, QUERY_FILE_4])
        self.exif.set_meta_data(QUERY_FILE_1, md.MetaData([QUERY_TAG_1, QUERY_TAG_2]))
        self.exif.set_meta_data(QUERY_FILE_2, md.MetaData([QUERY_TAG_2, QUERY_TAG_3]))
        self.exif.set_meta_data(QUERY_FILE_3, md.MetaData([QUERY_TAG_3, QUERY_TAG_4]))
        self.exif.set_meta_data(QUERY_FILE_4, md.MetaData([QUERY_TAG_4]))
        self.index.update(QUERY_FILE_1)
        self.index.update(QUERY_FILE_2)
        self.index.update(QUERY_FILE_3)
        self.index.update(QUERY_FILE_4)

    def test_list(self):
        tags = self.tie_core.list([READ_FILE_MD])
        self.assertEqual([TEST_READ_TAG_1.lower(), TEST_READ_TAG_2.lower()], tags, "listed tags do not match")

    def test_list_multiple_files(self):
        tags = self.tie_core.list([READ_FILE_MD, READ_FILE_MD_2])
        self.assertEqual(sorted([TEST_READ_TAG_1.lower(), TEST_READ_TAG_2.lower(), TEST_READ_TAG_3.lower()]), tags, "listed tags do not match")

    def test_list_empty_raw(self):
        cli.run_cmd(["cp", READ_FILE, WRITE_FILE])
        ee._write_exif_field("Exif.Photo.UserComment", "", WRITE_FILE)
        tags = self.tie_core.list([WRITE_FILE])
        self.assertEqual([], tags, "listed tags do not match empty list")
        os.remove(WRITE_FILE)

    def test_list_empty_md(self):
        cli.run_cmd(["cp", READ_FILE_MD, WRITE_FILE_MD])
        self.tie_core.clear(WRITE_FILE_MD)
        tags = self.tie_core.list([WRITE_FILE_MD])
        self.assertEqual([], tags, "listed tags do not match empty list")
        os.remove(WRITE_FILE_MD)

    def test_list_invalid(self):
        self.assertRaises(InvalidMetaDataError, lambda: self.tie_core.list([READ_FILE]))

    def test_list_not_found(self):
        self.assertRaises(FileNotFoundError, lambda: self.tie_core.list(["../res/foobar.not.existant"]))

    def test_tag(self):
        cli.run_cmd(["cp", READ_FILE_MD, WRITE_FILE_MD])
        added_tag1 = "New tag Ä"
        added_tag2 = "Other tag Ä"
        self.tie_core.tag(WRITE_FILE_MD, [added_tag1, added_tag2])
        self.assertEqual(sorted([TEST_READ_TAG_1.lower(), TEST_READ_TAG_2.lower(), added_tag1.lower(), added_tag2.lower()]), self.tie_core.list([WRITE_FILE_MD]), "Tags after adding did not match")
        os.remove(WRITE_FILE_MD)

    def test_tag_invalid(self):
        self.assertRaises(InvalidMetaDataError, lambda: self.tie_core.tag(READ_FILE, [TEST_READ_TAG_1]))

    def test_tag_duplicate(self):
        cli.run_cmd(["cp", READ_FILE_MD, WRITE_FILE_MD])
        added_tag1 = "New tag Ä"
        self.tie_core.tag(WRITE_FILE_MD, [added_tag1, added_tag1, TEST_READ_TAG_1])
        self.assertEqual(sorted([TEST_READ_TAG_1.lower(), TEST_READ_TAG_2.lower(), added_tag1.lower()]), self.tie_core.list([WRITE_FILE_MD]), "Tags after duplicate adding did not match")
        os.remove(WRITE_FILE_MD)

    def test_tag_not_found(self):
        self.assertRaises(FileNotFoundError, lambda: self.tie_core.tag("../res/foobar.not.existant", [TEST_READ_TAG_1]))

    def test_untag(self):
        cli.run_cmd(["cp", READ_FILE_MD, WRITE_FILE_MD])
        self.tie_core.untag(WRITE_FILE_MD, [TEST_READ_TAG_1])
        self.assertEqual([TEST_READ_TAG_2.lower()], self.tie_core.list([WRITE_FILE_MD]), "Tags after removing did not match")
        os.remove(WRITE_FILE_MD)

    def test_untag_duplicate(self):
        cli.run_cmd(["cp", READ_FILE_MD, WRITE_FILE_MD])
        self.tie_core.untag(WRITE_FILE_MD, [TEST_READ_TAG_1])
        self.tie_core.untag(WRITE_FILE_MD, [TEST_READ_TAG_1])
        self.tie_core.untag(WRITE_FILE_MD, [TEST_READ_TAG_1, TEST_READ_TAG_1])
        self.assertEqual([TEST_READ_TAG_2.lower()], self.tie_core.list([WRITE_FILE_MD]), "Tags after duplicate removing did not match")
        os.remove(WRITE_FILE_MD)

    def test_untag_invalid(self):
        self.assertRaises(InvalidMetaDataError, lambda: self.tie_core.untag(READ_FILE, [TEST_READ_TAG_1]))

    def test_untag_not_found(self):
        self.assertRaises(FileNotFoundError, lambda: self.tie_core.untag("../res/foobar.not.existant", [TEST_READ_TAG_1]))

    def test_clear(self):
        cli.run_cmd(["cp", READ_FILE_MD, WRITE_FILE_MD])
        self.tie_core.clear(WRITE_FILE_MD)
        tags_after_clear = self.tie_core.list([WRITE_FILE_MD])
        self.assertEqual([], tags_after_clear, "Tag list was not empty after clear")
        os.remove(WRITE_FILE_MD)

    def test_clear_invalid(self):
        cli.run_cmd(["cp", READ_FILE, WRITE_FILE])
        self.tie_core.clear(WRITE_FILE)
        tags_after_clear = self.tie_core.list([WRITE_FILE])
        self.assertEqual([], tags_after_clear, "Tag list was not empty after clearing corrupt file")
        os.remove(WRITE_FILE)

    def test_clear_not_found(self):
        self.assertRaises(FileNotFoundError, lambda: self.tie_core.clear("../res/foobar.not.existant"))

    def test_index(self):
        self.tie_core.update_index(READ_FILE_MD)
        link_name = self.files_base_path + ":" + "read_md.jpg"
        self.assertTrue(os.path.islink(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_1.lower(), link_name)),
                        "no link in tagdir 1")
        self.assertTrue(os.path.islink(os.path.join(TEST_INDEX_LOCATION, "tags", TEST_READ_TAG_2.lower(), link_name)),
                        "no link in tagdir 2")

    def test_list_all_tags(self):
        cli.run_cmd(["cp", READ_FILE_MD, WRITE_FILE_MD])
        self.tie_core.update_index(WRITE_FILE_MD)
        tags = self.tie_core.list_all_tags()
        self.assertEqual(sorted([TEST_READ_TAG_1.lower(), TEST_READ_TAG_2.lower()]), sorted(tags))
        os.remove(WRITE_FILE_MD)


def _path_to_linkname(img):
    return img.replace(os.sep, ":")


def _remove_index():
    cli.run_cmd(["rm", "-rf", TEST_INDEX_LOCATION])


def _clean_after_query_test():
    os.remove(QUERY_FILE_1)
    os.remove(QUERY_FILE_2)
    os.remove(QUERY_FILE_3)
    os.remove(QUERY_FILE_4)
