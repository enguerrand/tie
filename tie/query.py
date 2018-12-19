from typing import List
from enum import Enum


class QueryType(Enum):
    match_all = 1
    match_any = 2


class Query:
    def __init__(self, tags: List[str], query_type: QueryType):
        self.tags = tags
        self.query_type = query_type
