from json import JSONDecodeError
from subprocess import CalledProcessError

from pytag import cli
import pytag.meta_data as md


class ExifEditor:

    def __init__(self, field_name="Exif.Photo.UserComment"):
        self._field_name = field_name

    def get_meta_data(self, path: str) -> md.MetaData:
        """
            Raises: InvalidMetaData if the exiv data of the file could not be parsed
        """
        try:
            serialized = _read_exif_field(self._field_name, path)
        except CalledProcessError as e:
            if _is_file_not_found(e):
                raise e
            else:
                return md.empty()
        try:
            return md.deserialize(serialized)
        except JSONDecodeError as json_decode_error:
            raise md.InvalidMetaData(json_decode_error)

    def set_meta_data(self, path: str, data: md.MetaData):
        _write_exif_field(self._field_name, data.serialize(), path)


def _is_file_not_found(error: CalledProcessError):
    return error.returncode == 255


def _read_exif_field(field_name: str, path: str) -> str:
    std_out_lines = cli.run_cmd(["exiv2", "-K", field_name, path])
    return " ".join(std_out_lines[0].split()[3:])


def _write_exif_field(field_name: str, value: str, path: str):
    cli.run_cmd(['exiv2', '-M', 'set ' + field_name + ' ' + value, path])
