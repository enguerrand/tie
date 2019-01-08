from typing import List

from lib.abstract_frontend import Frontend


class FrontendBatch(Frontend):
    def get_user_confirmation(self, prompt: str) -> bool:
        return True

    def get_tags(self, available_tags: List[str]) -> List[str]:
        return []
