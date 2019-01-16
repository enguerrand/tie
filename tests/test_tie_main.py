import os
from typing import List
from unittest import TestCase

from lib import tie_main, cli, exif_editor
from lib.exif_editor import ExifEditor
from lib.index import Index
from lib.options_parser import Action, RunOptions, ParseError
from lib.tie_core import TieCoreImpl
from tests.frontend_test import FrontendTest, FrontendAdapter
from tests.test_index import TEST_INDEX_LOCATION, READ_FILE, WRITE_FILE, TEST_READ_VALUE_FIELD, WHITE_SPACE_FILE_MD, \
    READ_FILE_MD_NO_TAGS
from tests.tie_core_test_impl import TieCoreTestImpl, TieCoreAdapter


class TestTieMain(TestCase):
    def setUp(self):
        self.frontend = FrontendTest(True, ["foo", "bar"])

    def test_query(self):
        core = TieCoreTestImpl(Action.query, ["foo", "bar"], [])
        tie_main.run(core, RunOptions(["query", "foo", "bar"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_query_interactive_tags(self):
        core = TieCoreTestImpl(Action.query, ["foo", "bar"], [])
        tie_main.run(core, RunOptions(["query"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_query_no_tags(self):
        core = TieCoreTestImpl(Action.query, [], [])
        self.assertRaises(ParseError, lambda: tie_main.run(core, RunOptions(["query"]), FrontendTest(True, [])))

    def test_list(self):
        core = TieCoreTestImpl(Action.list, [], ["testfile"])
        tie_main.run(core, RunOptions(["list", "-f", "testfile"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_tag(self):
        # Duplicates in constructor calls account for repeated calls to method
        core = TieCoreTestImpl(Action.tag, ["foo", "bar", "foo", "bar"], ["testfile1", "testfile1", "testfile2", "testfile2"])
        tie_main.run(core, RunOptions(["tag", "foo", "bar", "-f", "testfile1", "testfile2"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_tag_white_space(self):
        # Duplicates in constructor calls account for repeated calls to method
        core = TieCoreTestImpl(Action.tag, ["foo"], [WHITE_SPACE_FILE_MD, WHITE_SPACE_FILE_MD])
        tie_main.run(core, RunOptions(["tag", "foo", "-f", WHITE_SPACE_FILE_MD]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_untag_file_without_tags(self):
        core = TieCoreAdapter()
        self.assertRaises(ParseError, lambda: tie_main.run(core, RunOptions(["untag", "-f", READ_FILE_MD_NO_TAGS]), self.frontend))

    def test_untag(self):
        # Duplicates in constructor calls account for repeated calls to method
        core = TieCoreTestImpl(Action.untag, ["foo", "bar", "foo", "bar"], ["testfile1", "testfile1", "testfile2", "testfile2"])
        tie_main.run(core, RunOptions(["untag", "foo", "bar", "-f", "testfile1", "testfile2"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_untag_interactive(self):
        user_choice = ["foo", "bar"]
        present_tags = ["foo", "bar", "bas"]

        class FrontendAnon(FrontendAdapter):
            def __init__(self):
                self.provided_options = []

            def get_tags(self, available_tags: List[str], allow_custom_tags) -> List[str]:
                self.provided_options = available_tags
                return user_choice

        class TieCoreTestInteractiveUntag(TieCoreAdapter):
            def __init__(self):
                self.untagged_file = ""
                self.removed_tags = ""

            def list(self, files: List[str]) -> List[str]:
                return present_tags

            def untag(self, file: str, tags: List[str]):
                self.untagged_file = file
                self.removed_tags = tags

        frontend = FrontendAnon()
        core = TieCoreTestInteractiveUntag()
        tie_main.run(core, RunOptions(["untag", "-f", "testfile1"]), frontend)
        self.assertEqual(sorted(present_tags), frontend.provided_options, "wrong options were provided")
        self.assertEqual(user_choice, core.removed_tags, "wrong tags were removed")

    def test_untag_interactive_multiple_files(self):
        user_choice = ["foo", "bas"]
        file_1 = "file1"
        file_2 = "file2"

        class FrontendAnon(FrontendAdapter):
            def __init__(self):
                self.provided_options = []

            def get_tags(self, available_tags: List[str], allow_custom_tags) -> List[str]:
                self.provided_options = available_tags
                return user_choice

        class TieCoreTestInteractiveUntag(TieCoreAdapter):
            def __init__(self):
                self.untagged_files = list()
                self.removed_tags = list()

            def list(self, files: List[str]) -> List[str]:
                return ["foo", "bar", "bas", "bam"]

            def untag(self, file: str, tags: List[str]):
                self.untagged_files.append(file)
                for t in tags:
                    self.removed_tags.append(t)

        frontend = FrontendAnon()
        core = TieCoreTestInteractiveUntag()
        tie_main.run(core, RunOptions(["untag", "-f", file_1, file_2]), frontend)
        self.assertEqual(sorted(["foo", "bar", "bas", "bam"]), frontend.provided_options, "wrong options were provided")
        self.assertEqual([file_1, file_2], core.untagged_files, "wrong files untagged")
        self.assertEqual(["foo", "bas", "foo", "bas"], core.removed_tags, "wrong tags were removed")

    def test_clear(self):
        core = TieCoreTestImpl(Action.clear, [], ["testfile1", "testfile1", "testfile2", "testfile2"])
        tie_main.run(core, RunOptions(["clear", "-f", "testfile1", "testfile2"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_index(self):
        core = TieCoreTestImpl(Action.index, [], ["testfile1", "testfile2"])
        tie_main.run(core, RunOptions(["index", "-f", "testfile1", "testfile2"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_tag_invalid_meta_data_file_confirmed(self):
        try:
            _remove_index()
            _setup_tag_invalid_meta_data_file(True)
            self.assertEqual('{"tags": ["foo"], "ver": 1}', exif_editor._read_exif_field("Exif.Photo.UserComment", WRITE_FILE))
        finally:
            _remove_index()
            os.remove(WRITE_FILE)

    def test_tag_invalid_meta_data_file_cancelled(self):
        try:
            _remove_index()
            _setup_tag_invalid_meta_data_file(False)
            self.assertEqual(TEST_READ_VALUE_FIELD, exif_editor._read_exif_field("Exif.Photo.UserComment", WRITE_FILE))
        finally:
            _remove_index()
            os.remove(WRITE_FILE)


def _setup_tag_invalid_meta_data_file(confirm_nuke):
    exif = ExifEditor("Exif.Photo.UserComment")
    index = Index(TEST_INDEX_LOCATION, exif)
    core = TieCoreImpl(exif, index)
    cli.run_cmd(["cp", READ_FILE, WRITE_FILE])
    frontend = FrontendTest(confirm_nuke, [])
    tie_main.run(core, RunOptions(["tag", "foo", WRITE_FILE]), frontend)


def _remove_index():
    cli.run_cmd(["rm", "-rf", TEST_INDEX_LOCATION])
