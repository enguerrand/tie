from pytag import cli
import pytag.meta_data as md

_field_name="Exif.Photo.UserComment"


def _read_exif_field(field_name: str, path: str) -> str:
    std_out_lines = cli.run_cmd(["exiv2", "-K", field_name, path])
    return " ".join(std_out_lines[0].split()[3:])


def _write_exif_field(field_name: str, value: str, path: str):
    cli.run_cmd(['exiv2', '-M', 'set ' + field_name + ' ' + value, path])


def get_meta_data(path: str) -> md.MetaData:
    serialized = _read_exif_field(_field_name, path)
    return md.deserialize(serialized)


def set_meta_data(path: str, data: md.MetaData):
    _write_exif_field(_field_name, data.serialize(), path)
