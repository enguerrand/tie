from lib.abstract_frontend import Frontend
from lib.frontend_cli import FrontendCli
from lib.options_parser import FrontendType


def from_type(frontend_type: FrontendType) -> Frontend:
    if frontend_type == FrontendType.cli:
        return FrontendCli()
    raise NotImplementedError("Frontend Type "+frontend_type.name+" is not implemented yet!")
