import hashlib
import os
from shutil import copyfile
from subprocess import CalledProcessError
from unittest import TestCase

from lib import cli
import lib.exif_editor as ee
import lib.meta_data as md

from tests.defines import *


class TestExifEditor(TestCase):

    def setUp(self):
        self.ee = ee.ExifEditor("Exif.Photo.UserComment")

    def test_read_raw(self):
        value = ee._read_exif_field("Exif.Photo.UserComment", READ_FILE)
        self.assertEqual('Some string with \'ä\' and "quotes', value)

    def test_write_raw(self):
        cli.run_cmd(["cp", READ_FILE, WRITE_FILE])
        with open(WRITE_FILE, 'rb') as f:
            md5_pre = hashlib.md5(f.read()).hexdigest()

            self.assertEqual("011da2f7ff8114d10b35150c2e962b26", md5_pre)
            ee._write_exif_field("Exif.Photo.UserComment", "My Dummy Value öä ' \" ", WRITE_FILE)
            md5_post = hashlib.md5(f.read()).hexdigest()
            self.assertEqual("d41d8cd98f00b204e9800998ecf8427e", md5_post)
        os.remove(WRITE_FILE)

    def test_read_md(self):
        data = self.ee.get_meta_data(READ_FILE_MD)
        self.assertEqual("42", data.ver)
        self.assertEqual([TEST_READ_TAG_1.lower(), TEST_READ_TAG_2.lower()], data.tags)

    def test_read_invalid_md(self):
        invalid_jpg = "../res/invalid.jpg"
        copyfile(READ_FILE, invalid_jpg)
        self.assertRaises(md.InvalidMetaDataError, lambda: self.ee.get_meta_data(invalid_jpg))
        os.remove(invalid_jpg)

    def test_write_md(self):
        cli.run_cmd(["cp", READ_FILE_MD, WRITE_FILE_MD])
        with open(WRITE_FILE_MD, 'rb') as f:
            md5_pre = hashlib.md5(f.read()).hexdigest()

            self.assertEqual("197c10f162136a0fa984477eb911058d", md5_pre)
            self.ee.set_meta_data(WRITE_FILE_MD, md.MetaData([TEST_WRITE_TAG_1, TEST_WRITE_TAG_2], "42"))
            md5_post = hashlib.md5(f.read()).hexdigest()
            self.assertEqual("eebc838d12ba676fc6adab2d4d434889", md5_post)
        os.remove(WRITE_FILE_MD)

    def test_read_from_non_img(self):
        self.assertRaises(CalledProcessError, lambda: self.ee.get_meta_data("../res/foobar.txt"))

    def test_read_non_existant_file(self):
        self.assertRaises(FileNotFoundError, lambda: self.ee.get_meta_data("../res/fooba.txt"))

    def test_write_non_existant_file(self):
        self.assertRaises(FileNotFoundError, lambda: self.ee.set_meta_data("../res/fooba.txt", md.empty()))

    def test_write_unknown_image_type(self):
        self.assertRaises(ee.CalledProcessError, lambda: self.ee.set_meta_data("../res/foobar.txt", md.empty()))
