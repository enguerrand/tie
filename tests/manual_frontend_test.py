import string
from typing import List

from lib.abstract_frontend import Frontend
from lib.frontend_batch import FrontendBatch
from lib.frontend_cli import FrontendCli
from lib.frontend_gtk import FrontendGtk
from lib.options_parser import FrontendType
from lib.printing import printerr


def test_frontend_user_confirm(frontend: Frontend):
    choice = frontend.get_user_confirmation("Confirm?")
    printerr("Your choice: "+str(choice))


def test_frontend_get_tags(frontend: Frontend, tags_choice: List[str]):
    choice = frontend.get_tags(tags_choice, True)
    printerr("Your choice:")
    for t in choice:
        printerr(t)


type = FrontendType.cli

if type == FrontendType.batch:
    printerr("Testing batch frontend")
    test_frontend_get_tags(FrontendBatch(), ["foo", "bar", "foo bar"])
    test_frontend_user_confirm(FrontendBatch())
elif type == FrontendType.cli:
    test_frontend_get_tags(FrontendCli(), list(string.ascii_lowercase))
    test_frontend_user_confirm(FrontendCli())
elif type == FrontendType.gtk:
    #test_frontend_get_tags(FrontendGtk(), ["foo", "bar", "foo bar", "äöl"])
    test_frontend_get_tags(FrontendGtk(), list(string.ascii_lowercase))
    test_frontend_user_confirm(FrontendGtk())

