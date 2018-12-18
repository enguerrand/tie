import hashlib
import os
from subprocess import CalledProcessError
from shutil import copyfile
from unittest import TestCase

from pytag import cli
import pytag.exif_editor as ee
import pytag.meta_data as md

from tests.test_tags import *

read_file = "../res/read.jpg"
write_file = "../res/write.jpg"
read_file_md = "../res/read_md.jpg"
write_file_md = "../res/write_md.jpg"


class TestExifEditor(TestCase):

    def setUp(self):
        self.ee = ee.ExifEditor()

    def test_read_raw(self):
        value = ee._read_exif_field("Exif.Photo.UserComment", read_file)
        self.assertEqual('Some string with \'ä\' and "quotes', value)

    def test_write_raw(self):
        cli.run_cmd(["cp", read_file, write_file])
        with open(write_file, 'rb') as f:
            md5_pre = hashlib.md5(f.read()).hexdigest()

            self.assertEqual("011da2f7ff8114d10b35150c2e962b26", md5_pre)
            ee._write_exif_field("Exif.Photo.UserComment", "My Dummy Value öä ' \" ", write_file)
            md5_post = hashlib.md5(f.read()).hexdigest()
            self.assertEqual("d41d8cd98f00b204e9800998ecf8427e", md5_post)

    def test_read_md(self):
        data = self.ee.get_meta_data(read_file_md)
        self.assertEqual("42", data.ver)
        self.assertEqual([TEST_READ_TAG_1, TEST_READ_TAG_2], data.tags)

    def test_read_invalid_md(self):
        invalid_jpg = "../res/invalid.jpg"
        copyfile(read_file, invalid_jpg)
        self.assertRaises(md.InvalidMetaData, lambda: self.ee.get_meta_data(invalid_jpg))
        os.remove(invalid_jpg)

    def test_write_md(self):
        cli.run_cmd(["cp", read_file_md, write_file_md])
        with open(write_file_md, 'rb') as f:
            md5_pre = hashlib.md5(f.read()).hexdigest()

            self.assertEqual("197c10f162136a0fa984477eb911058d", md5_pre)
            self.ee.set_meta_data(write_file_md, md.MetaData("42", [TEST_WRITE_TAG_1, TEST_WRITE_TAG_2]))
            md5_post = hashlib.md5(f.read()).hexdigest()
            self.assertEqual("eebc838d12ba676fc6adab2d4d434889", md5_post)

    def test_read_from_non_img(self):
        data = self.ee.get_meta_data("../res/foobar.txt")
        self.assertEqual(md.current_version, data.ver)
        self.assertEqual([], data.tags)

    def test_read_non_existant_file(self):
        self.assertRaises(CalledProcessError, lambda: self.ee.get_meta_data("../res/fooba.txt"))
