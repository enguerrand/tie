from typing import List, Set

import tie.exif_editor as ee
import tie.meta_data as md
from tie.index import Index
from tie.query import Query, QueryType


class TieCore:
    def __init__(self, exif: ee.ExifEditor, index: Index):
        self.exif = exif
        self.index = index

    def query(self, query: Query) -> List[str]:
        if query.query_type == QueryType.match_all:
            return self._query_match_all(query.tags)
        else:
            return self._query_match_any(query.tags)

    def _query_match_all(self, tags: List[str]):
        if len(tags) == 0:
            return []
        files: Set[str] = set()
        for tag in tags:
            if len(files) == 0:
                files = set(self.index.list_files(tag))
            else:
                files.intersection_update(set(self.index.list_files(tag)))
            if len(files) == 0:
                return []
        return sorted(files)

    def _query_match_any(self, tags: List[str]):
        files: Set[str] = set()
        for tag in tags:
            files = files.union(set(self.index.list_files(tag)))
        return sorted(files)

    def list(self, file: str) -> List[str]:
        """
            :raises InvalidMetaDataError if the file to be read contains invalid meta data
                    FileNotFoundError if the file to be read could not be found
        """
        return sorted(self.exif.get_meta_data(file).tags)

    def tag(self, file: str, tags: List[str]):
        """
            :raises InvalidMetaDataError if the file to be edited contains invalid meta data
                    UnsupportedFileTypeError if the file type to be edited does not support exif data
                    FileNotFoundError if the file to be edited could not be found
        """
        lcase_tags = set(t.lower() for t in tags)
        buffer = set(self.exif.get_meta_data(file).tags).union(lcase_tags)
        self.exif.set_meta_data(file, md.MetaData(list(buffer)))

    def untag(self, file: str, tags: List[str]):
        """
            :raises InvalidMetaDataError if the file to be edited contains invalid meta data
                    UnsupportedFileTypeError if the file type to be edited does not support exif data
                    FileNotFoundError if the file to be edited could not be found
        """
        buffer = set(self.exif.get_meta_data(file).tags)
        for tag in tags:
            buffer.discard(tag.lower())
        self.exif.set_meta_data(file, md.MetaData(list(buffer)))

    def clear(self, file: str):
        """
            :raises FileNotFoundError if the file to be edited could not be found
        """
        self.exif.set_meta_data(file, md.empty())

    def update_index(self, file: str):
        self.index.update(file)
