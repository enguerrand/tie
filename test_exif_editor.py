import hashlib
from unittest import TestCase

from ExifEditor import ExifEditor
from cli import Cli

read_file = "./res/read.jpg"
write_file = "./res/write.jpg"


class TestExifEditor(TestCase):

    def setUp(self):
        self.cli = Cli()
        self.ee = ExifEditor()

    def test_read_foobar(self):
        value = self.ee.read_exif_field("Exif.Photo.UserComment", read_file)
        self.assertEqual('Some string with \'ä\' and "quotes', value)

    def test_write_foobar(self):
        self.cli.run_cmd(["cp", read_file, write_file])
        with open(write_file, 'rb') as f:
            md5_pre = hashlib.md5(f.read()).hexdigest()

            self.assertEqual("011da2f7ff8114d10b35150c2e962b26", md5_pre)
            self.ee.write_exif_field("Exif.Photo.UserComment", "My Dummy Value öä ' \" ", write_file)
            md5_post = hashlib.md5(f.read()).hexdigest()
            self.assertEqual("d41d8cd98f00b204e9800998ecf8427e", md5_post)

