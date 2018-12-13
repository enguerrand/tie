import json
from typing import List


class MetaData:
    def __init__(self, tags: List[str]):
        self.tags = tags

    def serialize(self) -> str:
        return json.dumps({"tags": self.tags})

    def deserialize(serialized: str):
        decoded = json.loads(serialized)
        md = MetaData(decoded["tags"])
        return md
