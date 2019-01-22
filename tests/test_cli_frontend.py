from unittest import TestCase

from lib.frontend_cli import ScrollModel


class TestCli(TestCase):

    def test_scroll_model_initial(self):
        sm = setup_scroll_model(3, 5, 0)
        self.assertEqual(0, sm.scroll_position, "scroll position")
        self.assertEqual(0, sm.cursor_position, "cursor position")
        self.assertEqual(0, sm.get_top(), "top position")
        self.assertEqual(2, sm.get_bottom(), "bottom position")

    def test_scroll_model_scroll_down1(self):
        sm = setup_scroll_model(3, 5, 1)
        self.assertEqual(0, sm.scroll_position, "scroll position")
        self.assertEqual(1, sm.cursor_position, "cursor position")
        self.assertEqual(0, sm.get_top(), "top position")
        self.assertEqual(2, sm.get_bottom(), "bottom position")

    def test_scroll_model_scroll_down3(self):
        sm = setup_scroll_model(3, 5, 3)
        self.assertEqual(1, sm.scroll_position, "scroll position")
        self.assertEqual(3, sm.cursor_position, "cursor position")
        self.assertEqual(1, sm.get_top(), "top position")
        self.assertEqual(3, sm.get_bottom(), "bottom position")

    def test_scroll_model_scroll_down4(self):
        sm = setup_scroll_model(3, 5, 4)
        self.assertEqual(2, sm.scroll_position, "scroll position")
        self.assertEqual(4, sm.cursor_position, "cursor position")
        self.assertEqual(2, sm.get_top(), "top position")
        self.assertEqual(4, sm.get_bottom(), "bottom position")

    def test_scroll_model_scroll_up1(self):
        sm = setup_scroll_model(3, 5, -1)
        self.assertEqual(2, sm.scroll_position, "scroll position")
        self.assertEqual(4, sm.cursor_position, "cursor position")
        self.assertEqual(2, sm.get_top(), "top position")
        self.assertEqual(4, sm.get_bottom(), "bottom position")

    def test_scroll_model_scroll_down5(self):
        sm = setup_scroll_model(3, 5, 5)
        self.assertEqual(0, sm.scroll_position, "scroll position")
        self.assertEqual(0, sm.cursor_position, "cursor position")
        self.assertEqual(0, sm.get_top(), "top position")
        self.assertEqual(2, sm.get_bottom(), "bottom position")

    def test_scroll_model_scroll_down4_up2(self):
        sm = setup_scroll_model(3, 5, 4)
        sm.handle_up()
        sm.handle_up()
        self.assertEqual(2, sm.scroll_position, "scroll position")
        self.assertEqual(2, sm.cursor_position, "cursor position")
        self.assertEqual(2, sm.get_top(), "top position")
        self.assertEqual(4, sm.get_bottom(), "bottom position")


def setup_scroll_model(visible_lines, total_lines, scroll_offset) -> ScrollModel:
    m = ScrollModel(visible_lines, total_lines)
    if scroll_offset < 0:
        for i in range(0, -scroll_offset):
            m.handle_up()
    elif scroll_offset > 0:
        for i in range(0, scroll_offset):
            m.handle_down()
    return m
