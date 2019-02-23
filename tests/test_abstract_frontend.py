# -*- coding: utf-8 -*-
from unittest import TestCase

from lib.abstract_frontend import UserReply
from lib.frontend_batch import FrontendBatch
from tests.frontend_test import FrontendTest


class TestAbstractFrontend(TestCase):

    def test_get_user_confirmation_true(self):
        frontend = FrontendBatch(True)
        self.assertTrue(frontend._get_user_confirmation_impl("foo", False).value)
        self.assertTrue(frontend._get_user_confirmation_impl("foo", False).remember)

    def test_get_user_confirmation_simple(self):
        frontend = FrontendTest(UserReply.no, list(), False)
        reply = frontend.get_user_confirmation("prompt")
        self.assertEqual(UserReply.no, reply, "wrong user answer")
        reply = frontend.get_user_confirmation("prompt", "whatever")
        self.assertEqual(UserReply.no, reply, "wrong user answer")
        self.assertEqual(2, frontend.user_confirmation_count, "wrong call count of user confirmation method")

    def test_get_user_confirmation_repeated_false(self):
        frontend = FrontendTest(UserReply.no, list(), False)
        reply = frontend.get_user_confirmation("prompt", "whatever")
        self.assertEqual(UserReply.no, reply, "wrong user answer")
        reply = frontend.get_user_confirmation("prompt", "whatever")
        self.assertEqual(UserReply.no, reply, "wrong user answer")
        self.assertEqual(2, frontend.user_confirmation_count, "wrong call count of user confirmation method")

    def test_get_user_confirmation_repeated_remember_false(self):
        frontend = FrontendTest(UserReply.no, list(), True)
        reply = frontend.get_user_confirmation("prompt", "whatever")
        self.assertEqual(UserReply.no, reply, "wrong user answer")
        reply = frontend.get_user_confirmation("prompt", "whatever")
        self.assertEqual(UserReply.no, reply, "wrong user answer")
        self.assertEqual(1, frontend.user_confirmation_count, "wrong call count of user confirmation method")

    def test_get_user_confirmation_repeated_true(self):
        frontend = FrontendTest(UserReply.yes, list(), False)
        reply = frontend.get_user_confirmation("prompt", "whatever")
        self.assertEqual(UserReply.yes, reply, "wrong user answer")
        reply = frontend.get_user_confirmation("prompt", "whatever")
        self.assertEqual(UserReply.yes, reply, "wrong user answer")
        self.assertEqual(2, frontend.user_confirmation_count, "wrong call count of user confirmation method")

    def test_get_user_confirmation_repeated_remember_true(self):
        frontend = FrontendTest(UserReply.yes, list(), True)
        reply = frontend.get_user_confirmation("prompt", "whatever")
        self.assertEqual(UserReply.yes, reply, "wrong user answer")
        reply = frontend.get_user_confirmation("prompt", "whatever")
        self.assertEqual(UserReply.yes, reply, "wrong user answer")
        self.assertEqual(1, frontend.user_confirmation_count, "wrong call count of user confirmation method")

    def test_get_user_confirmation_cancel(self):
        frontend = FrontendTest(UserReply.cancel, list(), True)
        reply = frontend.get_user_confirmation("prompt", "whatever")
        self.assertEqual(UserReply.cancel, reply, "wrong user answer")

