# -*- coding: utf-8 -*-
from lib.abstract_frontend import Frontend, UserReply
from lib.frontend_batch import FrontendBatch
from lib.frontend_cli import FrontendCli
from lib.frontend_gtk import FrontendGtk
from lib.options_parser import FrontendType


def from_type(frontend_type: FrontendType) -> Frontend:
    if frontend_type == FrontendType.cli:
        return FrontendCli()
    if frontend_type == FrontendType.gtk:
        return FrontendGtk()
    elif frontend_type == FrontendType.batch:
        return FrontendBatch()
    elif frontend_type == FrontendType.yes:
        return FrontendBatch(confirm=UserReply.yes)
    raise NotImplementedError("Frontend Type "+frontend_type.name+" is not implemented yet!")
