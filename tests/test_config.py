import os
from pathlib import Path
from unittest import TestCase

from lib import config
from lib.config import Configuration


class TestConfig(TestCase):

    def test_config_path_default(self):
        os.unsetenv("TIE_CONFIG_PATH")
        path = config._get_config_file_path()
        self.assertEqual(os.path.join(str(Path.home()), ".tie.ini"), path, "Default config file path")

    def test_config_defaults(self):
        c = Configuration()
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
        c = Configuration()
        c.update_from_file()
        self.assertEqual("Vendor.What.Ever", c.exif_field_name, "Wrong exif field name read from file")
        self.assertEqual("/home/foo/.tie/", c.index_path, "Wrong index path read from file")
        del os.environ["TIE_CONFIG_PATH"]
