# -*- coding: utf-8 -*-
from typing import List
from enum import Enum


class MatchType(Enum):
    all = 1
    any = 2


class Query:
    def __init__(self, tags: List[str], match_type: MatchType):
        self.tags = tags
        self.match_type = match_type
