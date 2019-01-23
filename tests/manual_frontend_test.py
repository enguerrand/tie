import string
from typing import List

from lib.abstract_frontend import Frontend
from lib.frontend_batch import FrontendBatch
from lib.frontend_cli import FrontendCli
from lib.frontend_gtk import FrontendGtk
from lib.options_parser import FrontendType
from lib.printing import printerr


def test_frontend_user_confirm(fe: Frontend):
    choice = fe.get_user_confirmation("Confirm?")
    printerr("Your choice: "+str(choice))


def test_frontend_get_tags(fe: Frontend, tags_choice: List[str]):
    choice = fe.get_tags(tags_choice, True)
    printerr("Your choice:")
    for t in choice:
        printerr(t)


def test_frontend_show_message(fe: Frontend, message: str):
    fe.show_message(message)


type = FrontendType.gtk


if type == FrontendType.cli:
    frontend = FrontendCli()
elif type == FrontendType.gtk:
    frontend = FrontendGtk()
else:
    frontend = FrontendBatch()

test_frontend_show_message(frontend, "This is a simple message")
test_frontend_user_confirm(frontend)
test_frontend_get_tags(frontend, list(string.ascii_lowercase))
