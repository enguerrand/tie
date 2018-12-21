from typing import List

from tie.query import Query
from tie.tie_core import TieCore


class TieCoreTestImpl(TieCore):
    def query(self, query: Query) -> List[str]:
        pass

    def list(self, file: str) -> List[str]:
        pass

    def tag(self, file: str, tags: List[str]):
        pass

    def untag(self, file: str, tags: List[str]):
        pass

    def clear(self, file: str):
        pass

    def update_index(self, file: str):
        pass
