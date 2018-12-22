from unittest import TestCase

from lib.options_parser import RunOptions, Action, FrontendType, ParseError
from lib.query import MatchType


class TestOptionsParser(TestCase):
    def test_query_no_tags(self):
        opts = RunOptions(["query"])
        self.assertEqual(Action.query, opts.action)
        self.assertEqual(True, opts.needs_tags(), "needs tags")
        self.assertEqual(FrontendType.cli, opts.frontend)
        self.assertEqual(MatchType.all, opts.match_type)

    def test_query_short_no_tags(self):
        opts = RunOptions(["q"])
        self.assertEqual(Action.query, opts.action)

    def test_query_no_tags_frontend_gtk(self):
        opts = RunOptions(["query", "--frontend", "gtk"])
        self.assertEqual(Action.query, opts.action)
        self.assertEqual(True, opts.needs_tags(), "needs tags")
        self.assertEqual(FrontendType.gtk, opts.frontend)
        self.assertEqual(MatchType.all, opts.match_type)

    def test_query_no_tags_frontend_batch(self):
        opts = RunOptions(["query", "-F", "batch"])
        self.assertEqual(FrontendType.batch, opts.frontend)
        self.assertEqual(MatchType.all, opts.match_type)

    def test_query(self):
        opts = RunOptions(["query", "tag 1", "tag 2"])
        self.assertEqual(Action.query, opts.action)
        self.assertEqual(["tag 1", "tag 2"], opts.tags)
        self.assertEqual(False, opts.needs_tags(), "needs tags")
        self.assertEqual(FrontendType.cli, opts.frontend)
        self.assertEqual(MatchType.all, opts.match_type)

    def test_query_match_any_short(self):
        opts = RunOptions(["query", "tag 1", "tag 2", "-m", "any"])
        self.assertEqual(MatchType.any, opts.match_type)

    def test_query_match_any_long(self):
        opts = RunOptions(["query", "tag 1", "tag 2", "--match-type", "any"])
        self.assertEqual(MatchType.any, opts.match_type)

    def test_list_no_files(self):
        self.assertRaises(ParseError, lambda: RunOptions(["list"]))

    def test_list_frontend_gtk_files_long(self):
        opts = RunOptions(["list", "--frontend", "gtk", "--files", "foo"])
        self.assertEqual(Action.list, opts.action)
        self.assertEqual(False, opts.needs_tags(), "needs tags")
        self.assertEqual(["foo"], opts.files, "needs files")
        self.assertEqual(FrontendType.gtk, opts.frontend)

    def test_list_short(self):
        opts = RunOptions(["l", "--files", "foo"])
        self.assertEqual(Action.list, opts.action)

    def test_list_frontend_gtk_files_short(self):
        opts = RunOptions(["list", "-F", "gtk", "-f", "bar"])
        self.assertEqual(Action.list, opts.action)
        self.assertEqual(False, opts.needs_tags(), "needs tags")
        self.assertEqual(["bar"], opts.files, "needs files")
        self.assertEqual(FrontendType.gtk, opts.frontend)

    def test_list_frontend_gtk_multiple_files(self):
        self.assertRaises(ParseError, lambda: RunOptions(["list", "-F", "gtk", "-f", "foo", "bar"]))

    def test_tag_frontend_cli_files_long(self):
        opts = RunOptions(["tag", "--files", "foo", "--frontend", "cli", "bar"])
        self.assertEqual(Action.tag, opts.action)
        self.assertEqual(True, opts.needs_tags(), "needs tags")
        self.assertEqual(["foo", "bar"], opts.files, "needs files")
        self.assertEqual(FrontendType.cli, opts.frontend)

    def test_tag_short(self):
        opts = RunOptions(["t", "--files", "foo"])
        self.assertEqual(Action.tag, opts.action)

    def test_tag_frontend_cli_files_short(self):
        opts = RunOptions(["tag", "-f", "foo", "bar", "-F", "cli"])
        self.assertEqual(Action.tag, opts.action)
        self.assertEqual(True, opts.needs_tags(), "needs tags")
        self.assertEqual(["foo", "bar"], opts.files, "needs files")
        self.assertEqual(FrontendType.cli, opts.frontend)

    def test_untag_frontend_cli_files_long(self):
        opts = RunOptions(["untag", "tag 1", "tag 2", "--files", "foo", "bar"])
        self.assertEqual(Action.untag, opts.action)
        self.assertEqual(["tag 1", "tag 2"], opts.tags)
        self.assertEqual(False, opts.needs_tags(), "needs tags")
        self.assertEqual(["foo", "bar"], opts.files, "needs files")
        self.assertEqual(FrontendType.cli, opts.frontend)

    def test_untag_short(self):
        opts = RunOptions(["u", "--files", "foo"])
        self.assertEqual(Action.untag, opts.action)

    def test_clear(self):
        opts = RunOptions(["clear", "--files", "foo", "bar"])
        self.assertEqual(Action.clear, opts.action)
        self.assertEqual(False, opts.needs_tags(), "needs tags")
        self.assertEqual(["foo", "bar"], opts.files, "needs files")
        self.assertEqual(FrontendType.cli, opts.frontend)

    def test_clear_short(self):
        opts = RunOptions(["c", "--files", "foo"])
        self.assertEqual(Action.clear, opts.action)

    def test_index(self):
        opts = RunOptions(["index", "--files", "foo", "bar"])
        self.assertEqual(Action.index, opts.action)
        self.assertEqual(False, opts.needs_tags(), "needs tags")
        self.assertEqual(["foo", "bar"], opts.files, "needs files")
        self.assertEqual(FrontendType.cli, opts.frontend)

    def test_index_short(self):
        opts = RunOptions(["i", "--files", "foo"])
        self.assertEqual(Action.index, opts.action)

    def test_index_no_files(self):
        self.assertRaises(ParseError, lambda: RunOptions(["index"]))

    def test_index_no_files_more_args(self):
        self.assertRaises(ParseError, lambda: RunOptions(["index", "foo", "bar"]))

    def test_invalid_action(self):
        self.assertRaises(ParseError, lambda: RunOptions(["blubb"]))

    def test_invalid_action_more_args(self):
        self.assertRaises(ParseError, lambda: RunOptions(["blubb", "bbla"]))

    def test_invalid_option(self):
        self.assertRaises(ParseError, lambda: RunOptions(["index", "--brr", "bar"]))

    def test_no_action(self):
        self.assertRaises(ParseError, lambda: RunOptions(["--files", "foo"]))
