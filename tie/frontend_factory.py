from tie.abstract_frontend import Frontend
from tie.frontend_cli import FrontendCli
from tie.options_parser import FrontendType


def from_type(frontend_type: FrontendType) -> Frontend:
    if frontend_type == FrontendType.cli:
        return FrontendCli()
    raise NotImplementedError("Frontend Type "+frontend_type.name+" is not implemented yet!")
