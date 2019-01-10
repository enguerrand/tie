from lib.abstract_frontend import Frontend
from lib.frontend_batch import FrontendBatch
from lib.frontend_cli import FrontendCli
from lib.options_parser import FrontendType


def from_type(frontend_type: FrontendType) -> Frontend:
    if frontend_type == FrontendType.cli:
        return FrontendCli()
    elif frontend_type == FrontendType.batch:
        return FrontendBatch()
    elif frontend_type == FrontendType.yes:
        return FrontendBatch(confirm=True)
    raise NotImplementedError("Frontend Type "+frontend_type.name+" is not implemented yet!")
