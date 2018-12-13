import json
from typing import List


class MetaData:
    def __init__(self, ver: str, tags: List[str]):
        self.ver = ver
        self.tags = tags

    def serialize(self) -> str:
        return json.dumps({"ver": self.ver, "tags": self.tags})


def deserialize(serialized: str):
    decoded = json.loads(serialized)
    md = MetaData(decoded["ver"], decoded["tags"])
    return md
