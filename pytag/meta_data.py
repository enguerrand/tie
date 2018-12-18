import json
from json import JSONDecodeError
from typing import List

current_version = 1


class MetaData:
    def __init__(self, tags: List[str], ver=current_version):
        self.tags = tags
        self.ver = ver

    def serialize(self) -> str:
        return json.dumps({"tags": self.tags, "ver": self.ver})


def deserialize(serialized: str):
    """
        Raises: InvalidMetaData if the exiv data of the file could not be parsed
    """
    try:
        decoded = json.loads(serialized)
    except JSONDecodeError as json_decode_error:
        raise InvalidMetaData(json_decode_error)
    try:
        md = MetaData(decoded["tags"], decoded["ver"])
    except KeyError as key_error:
        raise InvalidMetaData(key_error)
    return md


def empty():
    return MetaData([])


class InvalidMetaData(Exception):
    pass
