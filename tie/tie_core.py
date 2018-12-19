from typing import List

import tie.exif_editor as ee
import tie.meta_data as md
from tie.index import Index


class TieCore:
    def __init__(self, exif: ee.ExifEditor, index: Index):
        self.exif = exif
        self.index = index

    def query(self, query: str):
        # TODO: Implement
        pass

    def list(self, file: str) -> List[str]:
        """
            :raises InvalidMetaDataError if the file to be read contains invalid meta data
                    FileNotFoundError if the file to be read could not be found
        """
        return self.exif.get_meta_data(file).tags

    def tag(self, file: str, tags: List[str]):
        """
            :raises InvalidMetaDataError if the file to be edited contains invalid meta data
                    UnsupportedFileTypeError if the file type to be edited does not support exif data
                    FileNotFoundError if the file to be edited could not be found
        """
        buffer = self.exif.get_meta_data(file).tags
        for tag in tags:
            lcase_tag = tag.lower()
            if lcase_tag not in buffer:
                buffer.append(lcase_tag)
        self.exif.set_meta_data(file, md.MetaData(buffer))

    def untag(self, file: str, tags: List[str]):
        """
            :raises InvalidMetaDataError if the file to be edited contains invalid meta data
                    UnsupportedFileTypeError if the file type to be edited does not support exif data
                    FileNotFoundError if the file to be edited could not be found
        """
        buffer = self.exif.get_meta_data(file).tags
        for tag in tags:
            lcase_tag = tag.lower()
            while lcase_tag in buffer:
                buffer.remove(lcase_tag)
        self.exif.set_meta_data(file, md.MetaData(buffer))

    def clear(self, file: str):
        """
            :raises FileNotFoundError if the file to be edited could not be found
        """
        self.exif.set_meta_data(file, md.empty())

    def update_index(self, file: str):
        self.index.update(file)
