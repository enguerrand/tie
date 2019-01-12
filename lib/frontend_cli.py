import curses
from typing import List

from lib import printing
from lib.abstract_frontend import Frontend
from lib.multiple_choice import MultipleChoice
from lib.printing import printerr


class FrontendCli(Frontend):
    def get_tags(self, available_tags: List[str]) -> List[str]:
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
        while True:
            bail = _handle_multiple_choice_input(key, mc)
            if bail:
                break
            _print_multiple_choice(mc, prompt, stdscr)
            key = stdscr.getch()
    finally:
        _tear_down_curses_dialog(stdscr)
    return mc.selection


def _handle_multiple_choice_input(key, mc):
    if key == curses.KEY_UP:
        mc.focus_previous()
    elif key == curses.KEY_DOWN:
        mc.focus_next()
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


def _print_multiple_choice(mc: MultipleChoice, prompt: str, stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, prompt + "\n\n")
    for o in mc.options:
        _print_option(mc, o, stdscr)
    stdscr.addstr("\nUse cursor keys to move up and down, space to toggle selection, "
                  "q to cancel and return to confirm selection")


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
