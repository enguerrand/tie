from unittest import TestCase

from lib import autocomplete


class TestAutoComplete(TestCase):
    def test_get_alternatives(self):
        self.assertEqual(["foo", "foo bar"], autocomplete.get_auto_complete_alternatives("f", ["foo", "foo bar", "bar"]))

    def test_get_alternatives_no_match(self):
        self.assertEqual([], autocomplete.get_auto_complete_alternatives("z", ["foo", "foo bar", "bar"]))

    def test_extract_common_string(self):
        self.assertEqual("foo", autocomplete.extract_common_prefix(["foo1", "foo2", "foo3"]))

    def test_extract_common_string_different_lengths(self):
        self.assertEqual("foo", autocomplete.extract_common_prefix(["foo1", "foo2", "foobar3"]))

    def test_extract_common_string_no_match(self):
        self.assertEqual("", autocomplete.extract_common_prefix(["foo1", "foo2", "bar3"]))

    def test_extract_common_string_with_empty_string(self):
        self.assertEqual("", autocomplete.extract_common_prefix(["", "foo2", "bar3"]))

    def test_extract_common_string_with_empty_options(self):
        self.assertEqual("", autocomplete.extract_common_prefix([]))

    def test_extract_common_string_one_entry(self):
        self.assertEqual("bar3", autocomplete.extract_common_prefix(["bar3"]))

    def test_autocomplete(self):
        self.assertEqual("foobar", autocomplete.auto_complete("foo", ["foobar1", "foobar2", "foobar3"]))

    def test_autocomplete_empty(self):
        self.assertEqual("foo", autocomplete.auto_complete("foo", []))

    def test_autocomplete_currently_matching(self):
        self.assertEqual("foo", autocomplete.auto_complete("foo", ["foo", "foobar"]))
