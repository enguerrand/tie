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

    def _update_from_file(self):
        path = _get_config_file_path()
        ini = _read_config_file(path)
        self.exif_field_name = _get_section_value_or_default(ini, EXIV2_SECTION, 'exif_field', self.exif_field_name)
        self.index_path = _get_section_value_or_default(ini, GENERAL_SECTION, 'index_path', self.index_path)


def _get_section_value_or_default(config: cp.ConfigParser, section_name: str, field_name: str,  fallback: str) -> str:
    try:
        section = config[section_name]
        return section[field_name]
    except KeyError:
        return fallback


def _get_config_file_path() -> str:
    try:
        return os.environ[ENV_VAR_CONFIG_FILE]
    except KeyError:
        return os.path.join(str(Path.home()), ".tie.ini")


def _read_config_file(path: str) -> cp.ConfigParser:
    config_parser = cp.ConfigParser()
    try:
        config_parser.read(path)
    except FileNotFoundError:
        pass
    return config_parser


def _read_file_contents(path) -> str:
    content = ""
    try:
        with open(path) as f:
            content += f.read()
    except FileNotFoundError:
        pass
    return content


def get_default_config() -> Configuration:
    return Configuration()


def load_user_config() -> Configuration:
    c = get_default_config()
    c._update_from_file()
    return c
