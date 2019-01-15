from typing import List

from lib.options_parser import Action
from lib.query import Query
from lib.tie_core import TieCore


class TieCoreTestImpl(TieCore):
    def __init__(self, action_type: Action, tags: List[str], files: List[str]):
        self.action_type = action_type
        self.tags = tags
        self.files = files

    def query(self, query: Query) -> List[str]:
        if self.action_type != Action.query:
            raise Exception("Wrong method called: query")
        for t in query.tags:
            self.tags.remove(t)
        return []

    def list(self, file: str) -> List[str]:
        if self.action_type != Action.list:
            raise Exception("Wrong method called: list")
        self.files.remove(file)
        return []

    def tag(self, file: str, tags: List[str]):
        if self.action_type != Action.tag:
            raise Exception("Wrong method called: tag")
        for t in tags:
            self.tags.remove(t)
        self.files.remove(file)
        return []

    def untag(self, file: str, tags: List[str]):
        if self.action_type != Action.untag:
            raise Exception("Wrong method called: untag")
        for t in tags:
            self.tags.remove(t)
        self.files.remove(file)

    def clear(self, file: str):
        if self.action_type != Action.clear:
            raise Exception("Wrong method called: clear")
        self.files.remove(file)

    def update_index(self, file: str):
        if self.action_type not in [Action.index, Action.tag, Action.untag, Action.clear]:
            raise Exception("Wrong method called: index")
        self.files.remove(file)

    def list_all_tags(self):
        pass

    def was_called_correctly(self):
        return len(self.tags) == 0 and len(self.files) == 0


class TieCoreAdapter(TieCore):

    def query(self, query: Query) -> List[str]:
        return list()

    def list(self, file: str) -> List[str]:
        return list()

    def tag(self, file: str, tags: List[str]):
        pass

    def untag(self, file: str, tags: List[str]):
        pass

    def clear(self, file: str):
        pass

    def update_index(self, file: str):
        pass

    def list_all_tags(self) -> List[str]:
        return list()
