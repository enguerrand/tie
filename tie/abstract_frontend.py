from abc import ABC, abstractmethod
from typing import List


class Frontend(ABC):

    @abstractmethod
    def get_tags(self) -> List[str]:
        pass
