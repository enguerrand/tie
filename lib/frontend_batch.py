from typing import List

from lib.abstract_frontend import Frontend
from lib.printing import print_out_list


class FrontendBatch(Frontend):

    def __init__(self, confirm=False):
        self.confirm = confirm

    def get_user_confirmation(self, prompt: str) -> bool:
        return self.confirm

    def get_tags(self, available_tags: List[str]) -> List[str]:
        return []

    def list_tags(self, file, tags):
        print_out_list(tags)
