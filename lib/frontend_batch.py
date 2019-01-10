from typing import List

from lib.abstract_frontend import Frontend


class FrontendBatch(Frontend):
    def __init__(self, confirm=False):
        self.confirm = confirm

    def get_user_confirmation(self, prompt: str) -> bool:
        return self.confirm

    def get_tags(self, available_tags: List[str]) -> List[str]:
        return []
