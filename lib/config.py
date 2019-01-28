# -*- coding: utf-8 -*-
import configparser as cp
import os
from pathlib import Path


ENV_VAR_CONFIG_FILE = 'TIE_CONFIG_PATH'
GENERAL_SECTION = 'GENERAL'
EXIV2_SECTION = 'EXIV2'

DEFAULT_EXIF_FIELD_NAME = "Exif.Photo.UserComment"


class Configuration:
    def __init__(self):
        self.exif_field_name = DEFAULT_EXIF_FIELD_NAME
        self.index_path = os.path.join(str(Path.home()), ".tie")
        self.exiv2_charset = 'UTF-8'
        self.exiv2_quiet = True
        self.exiv2_keep_time_stamps = True

    def _update_from_file(self):
        path = _get_config_file_path()
        ini = _read_config_file(path)
        self.index_path = _read_str_or_default(ini, GENERAL_SECTION, 'index_path', self.index_path)
        self.exif_field_name = _read_str_or_default(ini, EXIV2_SECTION, 'exif_field', self.exif_field_name)
        self.exiv2_charset = _read_str_or_default(ini, EXIV2_SECTION, 'charset', self.exiv2_charset)
        self.exiv2_quiet = _read_bool_or_default(ini, EXIV2_SECTION, 'quiet', self.exiv2_quiet)
        self.exiv2_keep_time_stamps = _read_bool_or_default(ini, EXIV2_SECTION, 'keep_time_stamps',
                                                            self.exiv2_keep_time_stamps)


def _read_str_or_default(config: cp.ConfigParser, section_name: str, field_name: str, fallback: str) -> str:
    try:
        section = config[section_name]
        return section[field_name]
    except KeyError:
        return fallback


def _read_bool_or_default(config: cp.ConfigParser, section_name: str, field_name: str, fallback: bool) -> bool:
    try:
        section = config[section_name]
        return section.getboolean(field_name)
    except KeyError:
        return fallback


def _get_config_file_path() -> str:
    try:
        return os.environ[ENV_VAR_CONFIG_FILE]
    except KeyError:
        return os.path.join(str(Path.home()), ".tie.ini")


def _read_config_file(path: str) -> cp.ConfigParser:
    config_parser = cp.ConfigParser()
    config_parser.read(path)
    return config_parser


def get_default_config() -> Configuration:
    return Configuration()


def load_user_config() -> Configuration:
    c = get_default_config()
    c._update_from_file()
    return c
