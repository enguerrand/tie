# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class UserReply(Enum):
    yes = 1
    no = 2
    cancel = 3


class UserConfirmation:
    def __init__(self, value: UserReply, remember: bool):
        self.value = value
        self.remember = remember


class Frontend(ABC):
    def __init__(self):
        self._user_confirmation_cache = dict()

    def get_user_confirmation(self, prompt: str, question_id=None) -> UserReply:
        if question_id is not None:
            propose_remember = True
            try:
                return self._user_confirmation_cache[question_id]
            except KeyError:
                pass
        else:
            propose_remember = False

        user_confirmation = self._get_user_confirmation_impl(prompt, propose_remember)
        if user_confirmation.remember and question_id is not None:
            self._user_confirmation_cache[question_id] = user_confirmation.value
        return user_confirmation.value

    @abstractmethod
    def _get_user_confirmation_impl(self, prompt: str, propose_remember: bool) -> UserConfirmation:
        pass

    @abstractmethod
    def get_tags(self, available_tags: List[str], allow_custom_tags) -> List[str]:
        pass

    @abstractmethod
    def list_tags(self, files: List[str], tags: List[str]):
        pass

    @abstractmethod
    def show_message(self, message: str):
        pass
