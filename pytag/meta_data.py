import json
from typing import List

current_version = 1


class MetaData:
    def __init__(self, tags: List[str], ver=current_version):
        self.tags = tags
        self.ver = ver

    def serialize(self) -> str:
        return json.dumps({"tags": self.tags, "ver": self.ver})


def deserialize(serialized: str):
    decoded = json.loads(serialized)
    md = MetaData(decoded["tags"], decoded["ver"])
    return md


def empty():
    return MetaData([])


class InvalidMetaData(Exception):
    pass
