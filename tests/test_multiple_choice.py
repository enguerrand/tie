# -*- coding: utf-8 -*-
from unittest import TestCase

from lib.multiple_choice import MultipleChoice


class TestMultipleChoice(TestCase):

    def test_sorted_options(self):
        mc = MultipleChoice(["def", "abc", "ghi"], True)
        self.assertEqual(["abc", "def", "ghi"], mc.options, "options not sorted")

    def test_has_option(self):
        mc = MultipleChoice(["def", "abc", "ghi"], True)
        self.assertTrue(mc.has_option("abc"))
        self.assertFalse(mc.has_option("jkm"))

    def test_focus_next(self):
        mc = MultipleChoice(["foo", "foo bar", "äöü"], True)
        self.assertEqual(0, mc.current_focus, "initial focus")
        self.assertTrue(mc.is_focused("foo"))
        self.assertFalse(mc.is_focused("foo bar"))
        mc.focus_next()
        self.assertEqual(1, mc.current_focus, "next focus")
        self.assertFalse(mc.is_focused("foo"))
        self.assertTrue(mc.is_focused("foo bar"))
        mc.focus_next()
        self.assertEqual(2, mc.current_focus, "next focus")
        mc.focus_next()
        self.assertEqual(0, mc.current_focus, "next focus")
        mc.focus_next()
        self.assertEqual(1, mc.current_focus, "next focus")

    def test_focus_prev(self):
        mc = MultipleChoice(["foo", "foo bar", "äöü"], True)
        self.assertEqual(0, mc.current_focus, "initial focus")
        mc.focus_previous()
        self.assertEqual(2, mc.current_focus, "prev focus")
        mc.focus_previous()
        self.assertEqual(1, mc.current_focus, "prev focus")
        mc.focus_previous()
        self.assertEqual(0, mc.current_focus, "prev focus")
        mc.focus_previous()
        self.assertEqual(2, mc.current_focus, "prev focus")

    def test_toggle_unselected(self):
        mc = MultipleChoice(["foo", "foo bar", "äöü"], True)
        mc.toggle_focused()
        self.assertTrue(mc.is_selected("foo"))

    def test_toggle_selected(self):
        mc = MultipleChoice(["foo", "foo bar", "äöü"], True)
        mc.select("foo")
        mc.toggle_focused()
        self.assertFalse(mc.is_selected("foo"))

    def test_multi_select_second_third(self):
        mc = MultipleChoice(["foo", "foo bar", "äöü"], True)
        mc.focus_next()
        mc.toggle_focused()
        mc.focus_next()
        mc.toggle_focused()
        self.assertFalse(mc.is_selected("foo"))
        self.assertTrue(mc.is_selected("foo bar"))
        self.assertTrue(mc.is_selected("äöü"))

    def test_single_select_second_then_first(self):
        mc = MultipleChoice(["foo", "foo bar", "äöü"], False)
        mc.focus_next()
        mc.toggle_focused()
        mc.focus_previous()
        mc.toggle_focused()
        self.assertTrue(mc.is_selected("foo"))
        self.assertFalse(mc.is_selected("foo bar"))
        self.assertFalse(mc.is_selected("äöü"))

    def test_empty_options(self):
        self.assertRaises(ValueError, lambda: MultipleChoice([], False))

    def test_add_custom_option(self):
        mc = MultipleChoice(["foo", "foo bar", "aöü"], True)
        mc.select("foo")
        mc.select("custom")
        self.assertEqual(["aöü", "custom", "foo",  "foo bar"], mc.options, "wrong options")
        self.assertEqual({"custom", "foo"}, mc.selection, "wrong selection")

    def test_add_custom_option_focus(self):
        mc = MultipleChoice(["abc", "fgh"], True)
        mc.focus_next()
        mc.select("def")
        self.assertEqual(["abc", "def", "fgh"], mc.options, "wrong options")
        self.assertEqual(2, mc.current_focus, "wrong focus")


