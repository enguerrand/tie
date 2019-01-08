import curses
import sys
from typing import List

from lib.abstract_frontend import Frontend
from lib.multiple_choice import MultipleChoice
from lib.printing import printerr, printstd


class FrontendCli(Frontend):
    def get_tags(self, available_tags: List[str]) -> List[str]:
        old_stdout = sys.stdout
        try:
            sys.stdout = sys.stderr
            return _multi_select("Please choose tags: ", available_tags)
        finally:
            sys.stdout = old_stdout

    def get_user_confirmation(self, prompt: str) -> bool:
        old_stdout = sys.stdout
        try:
            sys.stdout = sys.stderr
            user_input = input(prompt + " ").lower()
            while True:
                if user_input in ['y', 'j']:
                    return True
                elif user_input == 'n':
                    return False
                else:
                    printstd("\nInvalid input " + user_input + ". Please enter 'y' or 'n'.")
                    user_input = input(prompt + " ").lower()
        finally:
            sys.stdout = old_stdout


def _multi_select(prompt: str, options: List[str]):
    if len(options) == 0:
        return []

    stdscr = curses.initscr()
    curses.noecho()
    curses.setupterm()
    curses.cbreak()
    stdscr.keypad(True)

    mc = MultipleChoice(options, True)
    key = ''
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, prompt + "\n\n")
        if key == curses.KEY_UP:
            mc.focus_previous()
        elif key == curses.KEY_DOWN:
            mc.focus_next()
        elif key in [ord(' '), curses.KEY_RIGHT, curses.KEY_LEFT]:
            mc.toggle_focused()
        elif key == ord('q'):
            mc.clear_selection()
            break
        elif key in [curses.KEY_ENTER, ord('\n')]:
            break

        for o in options:

            if mc.is_selected(o):
                marker = "X"
            elif mc.is_focused(o):
                marker = "O"
            else:
                marker = "-"

            stdscr.addstr(marker + " " + o + "\n")

        stdscr.addstr("\nUse cursor key to move up and down, space to toggle selection, q to quit and return to finish")
        key = stdscr.getch()

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    return mc.selection # TODO sorting?


