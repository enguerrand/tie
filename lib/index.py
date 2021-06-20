# -*- coding: utf-8 -*-
import os
from subprocess import CalledProcessError

from lib import cli
import lib.exif_editor as ee
import lib.symlinks as sl
import lib.meta_data as md

TAGS_DIR_NAME = "tags"
SEPARATOR_PLACE_HOLDER = ":"


class Index:
    def __init__(self, root_dir: str, exif: ee.ExifEditor):
        self._exif = exif
        self._root_dir = root_dir
        self._tags_dir = os.path.join(self._root_dir, TAGS_DIR_NAME)
        _create_dir_if_absent(self._tags_dir)

    def list_tags(self):
        return sorted(os.listdir(self._tags_dir))

    def list_files(self, tag: str):
        files = []
        try:
            tag_dir = os.path.join(self._tags_dir, tag.lower())
            for link in os.listdir(tag_dir):
                link_path = os.path.join(tag_dir, link)
                if os.path.islink(link_path):
                    if sl.is_broken(link_path):
                        sl.rm(link_path)
                    else:
                        files.append(sl.readlink(link_path))
        except FileNotFoundError:
            pass
        return files

    def update(self, path: str):
        if os.path.isdir(path):
            self._update_dir_recursively(path)
        else:
            self._update_file(path)
        self._clean_obsolete_tags()

    def _update_dir_recursively(self, path):
        self._clear_orphaned_tags(path)
        for root, dirs, files in os.walk(path, followlinks=True):
            for file in files:
                self._update_file(os.path.join(root, file))
            for d in dirs:
                self._clear_orphaned_tags(d)

    def _update_file(self, path: str):
        try:
            meta_data = self._get_meta_data_safe(path)
            self._index_present_tags(meta_data, path)
            self._clear_absent_tags(meta_data, path)
        except FileNotFoundError:
            self._treat_as_missing_file(path)
            self._treat_missing_as_dir(path)

    def _get_meta_data_safe(self, path: str):
        try:
            return self._exif.get_meta_data(path)
        except md.InvalidMetaDataError:
            return md.empty()
        except CalledProcessError:
            return md.empty()

    def _treat_as_missing_file(self, path):
        self._clear_all_tags(path)

    def _treat_missing_as_dir(self, path):
        self._clear_tags_for_vanished_dir(path)

    def _index_present_tags(self, meta_data, path):
        for tag in meta_data.tags:
            absolute_tag_dir_path = _abspath(self._create_tag_if_absent(tag))
            absolute_file_path = _abspath(path)
            _create_tag(absolute_file_path, absolute_tag_dir_path)

    def _clear_all_tags(self, path):
        self._clear_absent_tags(md.empty(), path)

    def _clear_absent_tags(self, meta_data, path):
        link_name = _build_link_name(_abspath(path))
        for tag in self.list_tags():
            self._clear_tag_if_absent(tag, link_name, meta_data)

    def _create_tag_if_absent(self, tag: str) -> str:
        path = os.path.join(self._tags_dir, tag)
        _create_dir_if_absent(path)
        return path

    def _clear_tag_if_absent(self, tag_dir, link_name, meta_data):
        tag_name = os.path.basename(tag_dir)
        tag_path = _abspath(os.path.join(self._tags_dir, tag_name))
        if tag_name not in meta_data.tags:
            _clear_tag(tag_path, link_name)

    def _clear_tags_for_vanished_dir(self, vanished_dir: str):
        for t in self._find_tag_paths_pointing_into(vanished_dir):
            os.remove(t)

    def _clear_orphaned_tags(self, parent_dir: str):
        for t in self._find_tag_paths_pointing_into(parent_dir):
            destination = sl.readlink(t)
            if not os.path.isfile(destination):
                sl.rm(t)

    def _find_tag_paths_pointing_into(self, parent_dir: str):
        link_name_beginning = _build_link_name(_abspath(parent_dir)) + SEPARATOR_PLACE_HOLDER
        paths = []
        for tag in self.list_tags():
            tag_path = _abspath(os.path.join(self._tags_dir, tag))
            for link in os.listdir(tag_path):
                if link.startswith(link_name_beginning):
                    paths.append(os.path.join(tag_path, link))
        return paths

    def _clean_obsolete_tags(self):
        for tag in self.list_tags():
            tag_path = _abspath(os.path.join(self._tags_dir, tag))
            try:
                os.rmdir(tag_path)
            except OSError:
                # Directory was not empty. No need to handle error, we don't want to do anything in this case anyway
                pass


def _create_tag(absolute_file_path, absolute_tag_dir_path):
    sl.ln(absolute_file_path, _build_link_abs_path(absolute_tag_dir_path, absolute_file_path))


def _clear_tag(tag_path, link_name):
    try:
        os.remove(os.path.join(tag_path, link_name))
    except FileNotFoundError:
        pass


def _build_link_abs_path(abs_tagdir_path: str, abs_file_path: str):
    return os.path.join(abs_tagdir_path, _build_link_name(abs_file_path))


def _build_link_name(abs_file_path: str):
    return abs_file_path.replace(os.path.sep, SEPARATOR_PLACE_HOLDER)


def _create_dir_if_absent(path: str):
    cli.run_cmd(["mkdir", "-p", path])


def _abspath(p):
    return os.path.realpath(p)
