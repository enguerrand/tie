# -*- coding: utf-8 -*-
from unittest import TestCase

from lib.frontend_batch import FrontendBatch


class TestCli(TestCase):
    def setUp(self):
        self.frontend = FrontendBatch(False)

    def test_get_user_confirmation_false(self):
        frontend = FrontendBatch(False)
        self.assertEqual(False, frontend.get_user_confirmation("foo"))

    def test_get_user_confirmation_true(self):
        frontend = FrontendBatch(True)
        self.assertEqual(True, frontend.get_user_confirmation("foo"))

    def test_get_tags(self):
        frontend = FrontendBatch(True)
        self.assertEqual([], frontend.get_tags(["foo", "bar"], True))

    def test_list(self):
        # just check that it compiles
        frontend = FrontendBatch(True)
        frontend.list_tags(["file1", "file2"], ["tag1", "tag2"])
