# -*- coding: utf-8 -*-
import hashlib
import os
from shutil import copyfile
from subprocess import CalledProcessError
from unittest import TestCase

from lib import cli, exif_editor
import lib.meta_data as md
from lib.config import Configuration

from tests.defines import *


class TestExifEditor(TestCase):

    def setUp(self):
        self.ee = exif_editor.ExifEditor(Configuration())

    def test_read_raw(self):
        value = self.ee._read_exif_field("Exif.Photo.UserComment", READ_FILE)
        self.assertEqual('Some string with \'ä\' and "quotes', value)

    def test_write_raw(self):
        cli.run_cmd(["cp", READ_FILE, WRITE_FILE])
        with open(WRITE_FILE, 'rb') as f:
            md5_pre = hashlib.md5(f.read()).hexdigest()

        self.assertEqual("c14f5570050e188e897c4f1d030edff5", md5_pre)
        self.ee._write_exif_field("Exif.Photo.UserComment", "My Dummy Value öä ' \" ", WRITE_FILE)
        with open(WRITE_FILE, 'rb') as f:
            md5_post = hashlib.md5(f.read()).hexdigest()
            self.assertEqual("828d89558f1053c20daef859ce5f4634", md5_post)
        os.remove(WRITE_FILE)

    def test_read_md(self):
        data = self.ee.get_meta_data(READ_FILE_MD)
        self.assertEqual("42", data.ver)
        self.assertEqual([TEST_READ_TAG_1.lower(), TEST_READ_TAG_2.lower()], data.tags)

    def test_read_long_meta_data(self):
        cli.run_cmd(["cp", READ_FILE_MD, WRITE_FILE_MD])
        long_data = '{"tags": ["whatever", "words", "something", "this-is-long", "we-need-more-tags", "foobar", "lets", "see", "if", "this", "works"], "ver": 1}'
        with open(WRITE_FILE_MD, 'rb') as f:
            self.ee._write_exif_field("Exif.Photo.UserComment", long_data, WRITE_FILE_MD)
        written_md = self.ee.get_meta_data(WRITE_FILE_MD)
        self.assertEqual(["whatever", "words", "something", "this-is-long", "we-need-more-tags", "foobar", "lets", "see", "if", "this", "works"], written_md.tags)
        os.remove(WRITE_FILE_MD)

    def test_read_md_no_exif_data(self):
        self.assertRaises(CalledProcessError, lambda: self.ee.get_meta_data(READ_FILE_NO_EXIF))

    def test_read_md_safe_no_exif_data(self):
        result = self.ee.get_meta_data_safe(READ_FILE_NO_EXIF)
        self.assertEqual([], result.tags)

    def test_read_invalid_md(self):
        invalid_jpg = "../res/invalid.jpg"
        copyfile(READ_FILE, invalid_jpg)
        self.assertRaises(md.InvalidMetaDataError, lambda: self.ee.get_meta_data(invalid_jpg))
        os.remove(invalid_jpg)

    def test_write_md(self):
        cli.run_cmd(["cp", READ_FILE_MD, WRITE_FILE_MD])
        with open(WRITE_FILE_MD, 'rb') as f:
            md5_pre = hashlib.md5(f.read()).hexdigest()

            self.assertEqual("1daf4da69916978e5799fb446694549f", md5_pre)
            self.ee.set_meta_data(WRITE_FILE_MD, md.MetaData([TEST_WRITE_TAG_1, TEST_WRITE_TAG_2], "42"))
        with open(WRITE_FILE_MD, 'rb') as f:
            md5_post = hashlib.md5(f.read()).hexdigest()
            self.assertEqual("b2867d616bea116475c251d8be728825", md5_post)
        os.remove(WRITE_FILE_MD)

    def test_read_from_non_img(self):
        self.assertRaises(CalledProcessError, lambda: self.ee.get_meta_data("../res/foobar.txt"))

    def test_read_non_existant_file(self):
        self.assertRaises(FileNotFoundError, lambda: self.ee.get_meta_data("../res/fooba.txt"))

    def test_write_non_existant_file(self):
        self.assertRaises(FileNotFoundError, lambda: self.ee.set_meta_data("../res/fooba.txt", md.empty()))

    def test_write_unknown_image_type(self):
        self.assertRaises(exif_editor.CalledProcessError, lambda: self.ee.set_meta_data("../res/foobar.txt", md.empty()))
