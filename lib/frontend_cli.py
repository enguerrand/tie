from typing import List

from lib.abstract_frontend import Frontend
from lib.printing import printerr


class FrontendCli(Frontend):
    def get_tags(self) -> List[str]:
        printerr("Please choose tags: ")
        # TODO: Implement interactive user input
        return ["foobar"]

    def get_user_confirmation(self, prompt: str) -> bool:
        user_input = input(prompt).lower()
        return user_input in ['y', 'j']
