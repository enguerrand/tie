from unittest import TestCase

from lib import tie_main
from lib.frontend_batch import FrontendBatch
from lib.options_parser import Action, RunOptions
from tests.tie_core_test_impl import TieCoreTestImpl


class TestTieMain(TestCase):
    def setUp(self):
        self.frontend = FrontendBatch()

    def test_query(self):
        core = TieCoreTestImpl(Action.query, ["foo", "bar"], [])
        tie_main.run(core, RunOptions(["query", "foo", "bar"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_list(self):
        core = TieCoreTestImpl(Action.list, [], ["testfile"])
        tie_main.run(core, RunOptions(["list", "-f", "testfile"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_tag(self):
        # Duplicates in constructor calls account for repeated calls to method
        core = TieCoreTestImpl(Action.tag, ["foo", "bar", "foo", "bar"], ["testfile1", "testfile1", "testfile2", "testfile2"])
        tie_main.run(core, RunOptions(["tag", "foo", "bar", "-f", "testfile1", "testfile2"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_untag(self):
        # Duplicates in constructor calls account for repeated calls to method
        core = TieCoreTestImpl(Action.untag, ["foo", "bar", "foo", "bar"], ["testfile1", "testfile1", "testfile2", "testfile2"])
        tie_main.run(core, RunOptions(["untag", "foo", "bar", "-f", "testfile1", "testfile2"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_clear(self):
        core = TieCoreTestImpl(Action.clear, [], ["testfile1", "testfile1", "testfile2", "testfile2"])
        tie_main.run(core, RunOptions(["clear", "-f", "testfile1", "testfile2"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_index(self):
        core = TieCoreTestImpl(Action.index, [], ["testfile1", "testfile2"])
        tie_main.run(core, RunOptions(["index", "-f", "testfile1", "testfile2"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")
