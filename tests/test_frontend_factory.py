# -*- coding: utf-8 -*-
from unittest import TestCase

from lib import frontend_factory
from lib.frontend_batch import FrontendBatch
from lib.frontend_cli import FrontendCli
from lib.frontend_gtk import FrontendGtk
from lib.options_parser import FrontendType


class TestCli(TestCase):

    def test_batch(self):
        fe: FrontendBatch = frontend_factory.from_type(FrontendType.batch)
        self.assertIs(FrontendBatch, fe.__class__)
        self.assertIs(False, fe.confirm.value)
        self.assertIs(True, fe.confirm.remember)

    def test_yes(self):
        fe: FrontendBatch = frontend_factory.from_type(FrontendType.yes)
        self.assertIs(FrontendBatch, fe.__class__)
        self.assertIs(True, fe.confirm.value)
        self.assertIs(True, fe.confirm.remember)

    def test_cli(self):
        fe = frontend_factory.from_type(FrontendType.cli)
        self.assertIs(FrontendCli, fe.__class__)

    def test_gtk(self):
        fe = frontend_factory.from_type(FrontendType.gtk)
        self.assertIs(FrontendGtk, fe.__class__)

