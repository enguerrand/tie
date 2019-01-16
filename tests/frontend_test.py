from typing import List

from lib.abstract_frontend import Frontend
from lib.printing import print_out_list


class FrontendTest(Frontend):

    def __init__(self, user_confirmation: bool, interactive_tags: List[str]):
        self.user_confirmation = user_confirmation
        self.interactive_tags = interactive_tags

    def get_user_confirmation(self, prompt: str) -> bool:
        return self.user_confirmation

    def get_tags(self, available_tags: List[str], allow_custom_tags) -> List[str]:
        return self.interactive_tags

    def list_tags(self, files: List[str], tags: List[str]):
        print_out_list(tags)


class FrontendAdapter(Frontend):

    def get_user_confirmation(self, prompt: str) -> bool:
        return True

    def get_tags(self, available_tags: List[str], allow_custom_tags) -> List[str]:
        return list()

    def list_tags(self, files: List[str], tags: List[str]):
        pass
