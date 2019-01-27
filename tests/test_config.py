# -*- coding: utf-8 -*-
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
        self.assertEqual(os.path.join(str(Path.home()), ".tie"), c.index_path, "Index path does not match")

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
        d = dict()
        d['foo'] = "bar"
        self.assertEqual("bar", config._get_value_or_default(d, 'foo', 'bas'))
        self.assertEqual("bas", config._get_value_or_default(d, 'faa', 'bas'))
