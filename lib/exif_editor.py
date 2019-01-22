from subprocess import CalledProcessError

from lib import cli
import lib.meta_data as md
from tests.defines import EXIV2_WARN_ERROR_CODE


class ExifEditor:

    def __init__(self, field_name):
        self._field_name = field_name

    def get_meta_data(self, path: str) -> md.MetaData:
        """
            :raises CalledProcessError if the exiv2 command terminated abnormally
                    InvalidMetaDataError if the exiv data of the file could not be parsed
                    FileNotFoundError if the file could not be found
        """
        try:
            serialized = _read_exif_field(self._field_name, path)
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
            _write_exif_field(self._field_name, data.serialize(), path)
        except CalledProcessError as e:
            if _is_file_not_found(e):
                raise FileNotFoundError(e)
            else:
                raise e


def _is_file_not_found(error: CalledProcessError):
    return error.returncode == 255


def _read_exif_field(field_name: str, path: str) -> str:
    std_out_lines = cli.run_cmd(["exiv2", "-K", field_name, path], EXIV2_WARN_ERROR_CODE)
    return " ".join(std_out_lines[0].split()[3:])


def _write_exif_field(field_name: str, value: str, path: str):
    cli.run_cmd(['exiv2', '-M', 'set ' + field_name + ' ' + value, path])
