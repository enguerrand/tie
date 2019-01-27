# -*- coding: utf-8 -*-
import configparser
import os
import typing
from pathlib import Path


ENV_VAR_CONFIG_FILE = 'TIE_CONFIG_PATH'
GENERAL_SECTION = 'GENERAL'

DEFAULT_EXIF_FIELD_NAME = "Exif.Photo.UserComment"


class Configuration:
    def __init__(self):
        self.exif_field_name = DEFAULT_EXIF_FIELD_NAME
        self.index_path = os.path.join(str(Path.home()), ".tie")

    def _update_from_file(self):
        path = _get_config_file_path()
        ini = _read_section_less_config_file(path)
        settings = ini[GENERAL_SECTION]
        try:
            self.exif_field_name = settings['exif_field']
        except KeyError:
            pass
        try:
            self.index_path = settings['index_path']
        except KeyError:
            pass


def _get_value_or_default(settings: dict, name: str, fallback: str):
        try:
            return settings[name]
        except KeyError:
            return fallback


def _get_config_file_path() -> str:
    try:
        return os.environ[ENV_VAR_CONFIG_FILE]
    except KeyError:
        return os.path.join(str(Path.home()), ".tie.ini")


def _read_section_less_config_file(path: str) -> configparser.ConfigParser:
    section_header = '[' + GENERAL_SECTION + ']\n'
    content = section_header + _read_file_contents(path)
    config_parser = configparser.RawConfigParser()
    config_parser.read_string(content)
    return typing.cast(configparser.ConfigParser, config_parser)


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
