# -*- coding: utf-8 -*-
from unittest import TestCase

from lib.abstract_frontend import UserReply
from lib.frontend_batch import FrontendBatch


class TestCli(TestCase):
    def test_get_user_confirmation_false(self):
        frontend = FrontendBatch(UserReply.no)
        self.assertEqual(UserReply.no, frontend._get_user_confirmation_impl("foo", False).value)
        self.assertTrue(frontend._get_user_confirmation_impl("foo", False).remember)

    def test_get_user_confirmation_true(self):
        frontend = FrontendBatch(UserReply.yes)
        self.assertEqual(UserReply.yes, frontend._get_user_confirmation_impl("foo", False).value)
        self.assertTrue(frontend._get_user_confirmation_impl("foo", False).remember)

    def test_get_user_confirmation_cancel(self):
        frontend = FrontendBatch(UserReply.cancel)
        self.assertEqual(UserReply.cancel, frontend._get_user_confirmation_impl("foo", False).value)
        self.assertTrue(frontend._get_user_confirmation_impl("foo", False).remember)

    def test_get_tags(self):
        frontend = FrontendBatch(UserReply.yes)
        self.assertEqual([], frontend.get_tags(["foo", "bar"], True))

    def test_list(self):
        # just check that it compiles
        frontend = FrontendBatch(UserReply.yes)
        frontend.list_tags(["file1", "file2"], ["tag1", "tag2"])
