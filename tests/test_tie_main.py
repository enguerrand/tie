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
        core = TieCoreTestImpl(Action.tag, ["foo", "bar"], ["testfile"])
        tie_main.run(core, RunOptions(["tag", "foo", "bar", "-f", "testfile"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_untag(self):
        core = TieCoreTestImpl(Action.untag, ["foo", "bar"], ["testfile"])
        tie_main.run(core, RunOptions(["untag", "foo", "bar", "-f", "testfile"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_clear(self):
        core = TieCoreTestImpl(Action.clear, [], ["testfile"])
        tie_main.run(core, RunOptions(["clear", "-f", "testfile"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")

    def test_index(self):
        core = TieCoreTestImpl(Action.index, [], ["testfile"])
        tie_main.run(core, RunOptions(["index", "-f", "testfile"]), self.frontend)
        self.assertTrue(core.was_called_correctly(), "core was called incorrectly")
