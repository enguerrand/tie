import curses
from typing import List

from lib import printing
from lib.abstract_frontend import Frontend
from lib.multiple_choice import MultipleChoice
from lib.printing import printerr, print_out_list


class FrontendCli(Frontend):
    def get_tags(self, available_tags: List[str], allow_custom_tags) -> List[str]:
        backup_fd = printing.redirect_stdout()
        try:
            selected_tags = _multi_select("Please choose tags: ", available_tags)
            return selected_tags
        finally:
            printing.revert_stdout(backup_fd)

    def get_user_confirmation(self, prompt: str) -> bool:
        backup_fd = printing.redirect_stdout()
        try:
            user_input = input(prompt + " ").lower()
            while True:
                if user_input in ['y', 'j']:
                    return True
                elif user_input == 'n':
                    return False
                else:
                    printerr("\nInvalid input \'" + user_input + "\'. Please enter 'y' or 'n'.")
                    user_input = input(prompt + " ").lower()
        finally:
            printing.revert_stdout(backup_fd)

    def list_tags(self, files: List[str], tags: List[str]):
        print_out_list(tags)


class ScrollModel:
    def __init__(self, available_lines_count: int, displayed_lines_count: int):
        self.scroll_position = 0
        self.cursor_position = 0
        self.available_lines_count = available_lines_count
        self.displayed_lines_count = displayed_lines_count

    def handle_down(self):
        self.cursor_position = self.cursor_position + 1
        if self.cursor_position > self.displayed_lines_count-1:
            self.cursor_position = 0
            self.scroll_position = 0
        elif self.cursor_position - self.scroll_position >= self.available_lines_count - 1:
            self.scroll_position = self.scroll_position + 1

    def handle_up(self):
        self.cursor_position = self.cursor_position - 1
        if self.cursor_position < 0:
            self.cursor_position = self.displayed_lines_count - 1
            self.scroll_position = self.displayed_lines_count - self.available_lines_count + 1
        elif self.cursor_position < self.scroll_position:
            self.scroll_position = self.cursor_position

    def get_top(self) -> int:
        return self.scroll_position

    def get_bottom(self) -> int:
        return self.scroll_position + self.available_lines_count - 1


def _multi_select(prompt: str, options: List[str]):
    if len(options) == 0:
        return []

    mc = MultipleChoice(options, True)
    selected_options = _process_multiple_choice(mc, prompt)
    return selected_options


def _process_multiple_choice(mc, prompt):
    stdscr = _setup_curses_dialog()
    try:
        key = ''
        scroll = ScrollModel(curses.LINES - 4, len(mc.options))
        while True:
            bail = _handle_multiple_choice_input(key, mc, scroll)
            if bail:
                break
            _print_multiple_choice(mc, prompt, stdscr, scroll)
            key = stdscr.getch()
    finally:
        _tear_down_curses_dialog(stdscr)
    return mc.selection


def _handle_multiple_choice_input(key, mc: MultipleChoice, scroll: ScrollModel):
    if key == curses.KEY_UP:
        mc.focus_previous()
        scroll.handle_up()
    elif key == curses.KEY_DOWN:
        mc.focus_next()
        scroll.handle_down()
    elif key in [ord(' '), curses.KEY_RIGHT, curses.KEY_LEFT]:
        mc.toggle_focused()
    elif key == ord('q'):
        mc.clear_selection()
    return key in [curses.KEY_ENTER, ord('\n'), ord('q')]


def _setup_curses_dialog():
    stdscr = curses.initscr()
    curses.noecho()
    curses.setupterm()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr


def _tear_down_curses_dialog(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def _print_multiple_choice(mc: MultipleChoice, prompt: str, stdscr, scroll: ScrollModel):
    stdscr.clear()
    stdscr.addstr(0, 0, prompt + "\n\n")
    start = scroll.get_top()
    end = scroll.get_bottom()
    for o in mc.options[start:end]:
        _print_option(mc, o, stdscr)
    stdscr.addstr("\nCursor keys & space to select | q to cancel | enter to confirm")


def _print_option(mc: MultipleChoice, option: str, stdscr):
    marker = _get_option_marker(mc, option)
    stdscr.addstr(marker + " " + option + "\n")


def _get_option_marker(mc, option) -> str:
    if mc.is_selected(option) and mc.is_focused(option):
        return "-> (X)"
    elif mc.is_selected(option):
        return "   (X)"
    elif mc.is_focused(option):
        return "-> ( )"
    else:
        return "   ( )"
