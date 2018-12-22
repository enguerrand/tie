import sys
from typing import List

from lib.abstract_frontend import Frontend
from lib.printing import printerr, printstd


class FrontendCli(Frontend):
    def get_tags(self) -> List[str]:
        printerr("Please choose tags: ")
        # TODO: Implement interactive user input
        return ["foobar"]

    def get_user_confirmation(self, prompt: str) -> bool:
        old_stdout = sys.stdout
        try:
            sys.stdout = sys.stderr
            user_input = input(prompt + " ").lower()
            while True:
                if user_input in ['y', 'j']:  # TODO localize
                    return True
                elif user_input == 'n':
                    return False
                else:
                    printstd("\nInvalid input " + user_input + ". Please enter 'y' or 'n'.")
                    user_input = input(prompt + " ").lower()
        finally:
            sys.stdout = old_stdout
