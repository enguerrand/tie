# -*- coding: utf-8 -*-
from typing import List

from lib.abstract_frontend import Frontend, UserConfirmation, UserReply
from lib.printing import print_out_list, printerr


class FrontendTest(Frontend):

    def __init__(self, user_confirmation: UserReply, interactive_tags: List[str], remember=False):
        super().__init__()
        self.user_confirmation = UserConfirmation(user_confirmation, remember)
        self.interactive_tags = interactive_tags
        self.user_confirmation_count = 0

    def _get_user_confirmation_impl(self, prompt: str, propose_remember: bool) -> UserConfirmation:
        self.user_confirmation_count += 1
        return self.user_confirmation

    def get_tags(self, available_tags: List[str], allow_custom_tags) -> List[str]:
        return self.interactive_tags

    def list_tags(self, files: List[str], tags: List[str]):
        print_out_list(tags)

    def show_message(self, message: str):
        printerr(message)


class FrontendAdapter(Frontend):
    def __init__(self):
        super().__init__()

    def _get_user_confirmation_impl(self, prompt: str, propose_remember: bool) -> UserReply:
        return UserReply.yes

    def get_tags(self, available_tags: List[str], allow_custom_tags) -> List[str]:
        return list()

    def list_tags(self, files: List[str], tags: List[str]):
        pass

    def show_message(self, message: str):
        pass
