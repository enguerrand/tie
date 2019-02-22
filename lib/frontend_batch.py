# -*- coding: utf-8 -*-
from typing import List

from lib.abstract_frontend import Frontend, UserConfirmation, UserReply
from lib.printing import print_out_list, printerr


class FrontendBatch(Frontend):

    def __init__(self, confirm=UserReply.no):
        super().__init__()
        self.confirm = UserConfirmation(confirm, True)

    def _get_user_confirmation_impl(self, prompt: str, propose_remember: bool) -> UserConfirmation:
        return self.confirm

    def get_tags(self, available_tags: List[str], allow_custom_tags) -> List[str]:
        return []

    def list_tags(self, files: List[str], tags: List[str]):
        print_out_list(tags)

    def show_message(self, message: str):
        printerr(message)
