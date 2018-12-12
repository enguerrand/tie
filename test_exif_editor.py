import hashlib
from unittest import TestCase

from ExifEditor import ExifEditor
from Cli import Cli

read_file = "./res/read.jpg"
write_file = "./res/write.jpg"

class TestExifEditor(TestCase):

    def setUp(self):
        self.cli = Cli()
        self.ee = ExifEditor()

    def test_read_foobar(self):
        value = self.ee.read_exif_field("Exif.Photo.UserComment", read_file)
        self.assertEqual(value, "foobar")

    def test_write_foobar(self):
        self.cli.run_cmd(["cp", read_file, write_file])
        with open(write_file, 'rb') as f:
            md5_pre = hashlib.md5(f.read()).hexdigest()

            self.assertEqual(md5_pre, "b09c7fc16a9780f5939d60e76fc58739")
            self.ee.write_exif_field("Exif.Photo.UserComment", "My Dummy Value öä ' \" ", write_file)
            md5_post = hashlib.md5(f.read()).hexdigest()
            self.assertEqual(md5_post, "58f04929798e9df73f736b46942217a5")

