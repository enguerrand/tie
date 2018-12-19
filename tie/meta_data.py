import json
from json import JSONDecodeError
from typing import List

current_version = 1


class MetaData:
    def __init__(self, tags: List[str], ver=current_version):
        self.tags = [t.lower() for t in tags]
        self.ver = ver

    def serialize(self) -> str:
        return json.dumps({"tags": self.tags, "ver": self.ver})


def deserialize(serialized: str):
    """
        :raises InvalidMetaDataError if the exiv data of the file could not be parsed
    """
    if serialized.strip() == "":
        return empty()
    try:
        decoded = json.loads(serialized)
    except JSONDecodeError as json_decode_error:
        raise InvalidMetaDataError(json_decode_error)
    try:
        md = MetaData(decoded["tags"], decoded["ver"])
    except KeyError as key_error:
        raise InvalidMetaDataError(key_error)
    return md


def empty():
    return MetaData([])


class InvalidMetaDataError(Exception):
    pass
