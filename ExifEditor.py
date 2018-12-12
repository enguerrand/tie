from Cli import Cli


class ExifEditor:

    def __init__(self):
        self.cli = Cli()

    def read_exif_field(self, field_name, path):
        std_out_lines = self.cli.run_cmd(["exiv2", "-K", field_name, path])
        return std_out_lines[0].split()[3]

    def write_exif_field(self, field_name, value, path):
        self.cli.run_cmd(['exiv2', '-M', 'set ' + field_name + ' ' + value, path])
