from typing import List

from lib.abstract_frontend import Frontend
from lib.printing import print_out_list, printerr


class FrontendBatch(Frontend):

    def __init__(self, confirm=False):
        self.confirm = confirm

    def get_user_confirmation(self, prompt: str) -> bool:
        return self.confirm

    def get_tags(self, available_tags: List[str], allow_custom_tags) -> List[str]:
        return []

    def list_tags(self, files: List[str], tags: List[str]):
        print_out_list(tags)

    def show_message(self, message: str):
        printerr(message)
