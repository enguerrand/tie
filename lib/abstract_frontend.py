from abc import ABC, abstractmethod
from typing import List


class Frontend(ABC):
    @abstractmethod
    def get_user_confirmation(self, prompt: str) -> bool:
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
