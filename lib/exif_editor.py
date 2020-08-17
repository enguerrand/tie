# -*- coding: utf-8 -*-
from subprocess import CalledProcessError
from typing import List

from lib import cli
import lib.meta_data as md
from lib.config import Configuration
from tests.defines import EXIV2_WARN_ERROR_CODE


class ExifEditor:

    def __init__(self, config: Configuration):
        self._config = config

    def get_meta_data_safe(self, path: str) -> md.MetaData:
        """
            :raises InvalidMetaDataError if the exiv data of the file could not be parsed
                    FileNotFoundError if the file could not be found
        """
        try:
            return self.get_meta_data(path)
        except CalledProcessError:
            return md.empty()

    def get_meta_data(self, path: str) -> md.MetaData:
        """
            :raises CalledProcessError if the exiv2 command terminated abnormally
                    InvalidMetaDataError if the exiv data of the file could not be parsed
                    FileNotFoundError if the file could not be found
        """
        try:
            serialized = self._read_exif_field(self._config.exif_field_name, path)
        except CalledProcessError as e:
            if _is_file_not_found(e):
                raise FileNotFoundError(e)
            else:
                raise e
        return md.deserialize(serialized)

    def set_meta_data(self, path: str, data: md.MetaData):
        """
            :raises CalledProcessError if the exiv2 command terminated abnormally
                    FileNotFoundError if the file could not be found
        """
        try:
            self._write_exif_field(self._config.exif_field_name, data.serialize(), path)
        except CalledProcessError as e:
            if _is_file_not_found(e):
                raise FileNotFoundError(e)
            else:
                raise e

    def _read_exif_field(self, field_name: str, path: str) -> str:
        base = self._build_exiv_base_command()
        command = self._build_exiv_read_command(base, field_name, path)
        std_out_lines = cli.run_cmd(command, EXIV2_WARN_ERROR_CODE)
        return " ".join(std_out_lines[0].split()[3:])

    def _write_exif_field(self, field_name: str, value: str, path: str):
        base = self._build_exiv_base_command()
        command = self._build_exiv_write_command(base, field_name, value, path)
        cli.run_cmd(command)

    def _build_exiv_base_command(self) -> List[str]:
        cmd = ['exiv2', '-n', self._config.exiv2_charset]
        if self._config.exiv2_quiet:
            cmd.append('-q')
        return cmd

    def _build_exiv_read_command(self, base_command: List[str], field_name: str, path: str):
        base_command.append('-b')
        base_command.append('-K')
        base_command.append(field_name)
        base_command.append(path)
        return base_command

    def _build_exiv_write_command(self, base_command: List[str], field_name: str, value: str, path: str):
        if self._config.exiv2_keep_time_stamps:
            base_command.append('-k')
        base_command.append('-M')
        base_command.append('set ' + field_name + ' ' + value)
        base_command.append(path)
        return base_command


def _is_file_not_found(error: CalledProcessError):
    return error.returncode == 255
