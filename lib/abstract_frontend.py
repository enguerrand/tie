from abc import ABC, abstractmethod
from typing import List


class Frontend(ABC):
    @abstractmethod
    def get_user_confirmation(self, prompt: str) -> bool:
        pass

    @abstractmethod
    def get_tags(self, available_tags: List[str]) -> List[str]:
        pass
