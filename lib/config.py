import configparser
import os
import typing
from pathlib import Path

ENV_VAR_CONFIG_FILE = 'TIE_CONFIG_PATH'
GENERAL_SECTION = 'GENERAL'


class Configuration:
    def __init__(self):
        self.exif_field_name = "Exif.Photo.UserComment"
        self.index_path = os.path.join(str(Path.home()), ".tie")

    def _update_from_file(self):
        path = _get_config_file_path()
        ini = _read_section_less_config_file(path)
        try:
            settings = ini[GENERAL_SECTION]
            self.exif_field_name = settings['exif_field']
            self.index_path = settings['index_path']
        except KeyError:
            pass
        print(self.exif_field_name)


def _get_config_file_path() -> str:
    try:
        return os.environ[ENV_VAR_CONFIG_FILE]
    except KeyError:
        return os.path.join(str(Path.home()), ".tie.ini")


def _read_section_less_config_file(path: str) -> configparser.ConfigParser:
    content = _read_file_and_prepend_section_header(path)
    config_parser = configparser.RawConfigParser()
    config_parser.read_string(content)
    return typing.cast(configparser.ConfigParser, config_parser)


def _read_file_and_prepend_section_header(path) -> str:
    with open(path) as f:
        content = '[' + GENERAL_SECTION + ']\n' + f.read()
    return content


def get_default_config() -> Configuration:
    return Configuration()


def load_user_config() -> Configuration:
    c = get_default_config()
    c._update_from_file()
    return c
