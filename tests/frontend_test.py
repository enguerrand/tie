from typing import List

from lib.abstract_frontend import Frontend


class FrontendTest(Frontend):
    def __init__(self, user_confirmation: bool, interactive_tags: List[str]):
        self.user_confirmation = user_confirmation
        self.interactive_tags = interactive_tags

    def get_user_confirmation(self, prompt: str) -> bool:
        return self.user_confirmation

    def get_tags(self, available_tags: List[str]) -> List[str]:
        return self.interactive_tags
