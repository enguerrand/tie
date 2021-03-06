# -*- coding: utf-8 -*-
import configparser
import os
from pathlib import Path
from unittest import TestCase

from lib import config


class TestConfig(TestCase):

    def test_config_path_default(self):
        path = config._get_config_file_path()
        self.assertEqual(os.path.join(str(Path.home()), ".tie.ini"), path, "Default config file path")

    def test_config_defaults(self):
        c = config.get_default_config()
        self.assertEqual("Exif.Photo.UserComment", c.exif_field_name, "Default exif field name")
        self.assertEqual(os.path.join(str(Path.home()), ".tie"), c.index_path, "Default index path")
        self.assertEqual('UTF-8', c.exiv2_charset, "Default exiv2 charset")
        self.assertEqual(True, c.exiv2_quiet, "Default exiv2 quiet")
        self.assertEqual(True, c.exiv2_keep_time_stamps, "Default exiv2 keep timestamps")

    def test_config_file_location_from_envvar(self):
        os.environ["TIE_CONFIG_PATH"] = "/foo/bar"
        path = config._get_config_file_path()
        self.assertEqual("/foo/bar", path)
        del os.environ["TIE_CONFIG_PATH"]

    def test_config_file(self):
        cfp = "../res/testconfig.ini"
        os.environ["TIE_CONFIG_PATH"] = cfp
        self.assertEqual(cfp, config._get_config_file_path(), "Config file path from environment variable")
        c = config.load_user_config()
        self.assertEqual("Vendor.What.Ever", c.exif_field_name, "Wrong exif field name read from file")
        self.assertEqual("/home/foo/.tie/", c.index_path, "Wrong index path read from file")
        self.assertEqual('ISO_8859-1', c.exiv2_charset, "exiv2 charset read from file")
        self.assertEqual(False, c.exiv2_quiet, "exiv2 quiet read from file")
        self.assertEqual(False, c.exiv2_keep_time_stamps, "exiv2 keep timestamps read from file")
        del os.environ["TIE_CONFIG_PATH"]

    def test_config_file_missing_key(self):
        cfp = "../res/testconfig2.ini"
        os.environ["TIE_CONFIG_PATH"] = cfp
        self.assertEqual(cfp, config._get_config_file_path(), "Config file path from environment variable")
        c = config.load_user_config()
        self.assertEqual("Exif.Photo.UserComment", c.exif_field_name, "Default exif field name")
        self.assertEqual("/home/foo/.tie/", c.index_path, "Wrong index path read from file")
        del os.environ["TIE_CONFIG_PATH"]

    def test_config_file_not_found(self):
        os.environ["TIE_CONFIG_PATH"] = "/file/that/does/not/exist.tie"
        c = config.load_user_config()
        self.assertEqual(config.DEFAULT_EXIF_FIELD_NAME, c.exif_field_name, "Failed to fall back to default config")
        del os.environ["TIE_CONFIG_PATH"]

    def test_get_value_or_default(self):
        d = configparser.ConfigParser()
        d['foo'] = dict()
        d['foo']['bar'] = 'found'

        self.assertEqual("found", config._read_str_or_default(d, 'foo', 'bar', 'not_found'))
        self.assertEqual("not_found", config._read_str_or_default(d, 'faa', 'bas', 'not_found'))
