import os

from pytag import cli
import pytag.exif_editor as ee
import pytag.symlinks as sl

TAGS_DIR_NAME = "tags"
SEPARATOR_PLACE_HOLDER = ":"


class Index:
    def __init__(self, root_dir: str, exif: ee.ExifEditor):
        self._exif = exif
        self._root_dir = root_dir
        self._tags_dir = os.path.join(self._root_dir, TAGS_DIR_NAME)
        _create_dir_if_absent(self._tags_dir)

    def update(self, path: str):
        if os.path.isdir(path):
            self._update_dir_recursively(path)
        else:
            self._update_file(path)

    def _update_dir_recursively(self, path):
        for root, dirs, files in os.walk(path, followlinks=True):
            for file in files:
                self._update_file(os.path.join(root, file))

    def _update_file(self, path: str):
        meta_data = self._exif.get_meta_data(path)
        for tag in meta_data.tags:
            absolute_tag_dir_path = os.path.abspath(self._create_tag_if_absent(tag))
            absolute_file_path = os.path.abspath(path)
            sl.ln(absolute_file_path, self._build_link_abs_path(absolute_tag_dir_path, absolute_file_path))

    def _create_tag_if_absent(self, tag: str) -> str:
        path = os.path.join(self._tags_dir, tag)
        _create_dir_if_absent(path)
        return path

    def _build_link_abs_path(self, abs_tagdir_path: str, abs_file_path: str):
        return os.path.join(abs_tagdir_path, _build_link_name(abs_file_path))


def _build_link_name(abs_file_path: str):
        return abs_file_path.replace(os.path.sep, SEPARATOR_PLACE_HOLDER)


def _create_dir_if_absent(path: str):
    cli.run_cmd(["mkdir", "-p", path])


