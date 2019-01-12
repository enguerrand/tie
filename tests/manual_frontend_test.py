from typing import List

from lib.abstract_frontend import Frontend
from lib.frontend_batch import FrontendBatch
from lib.frontend_cli import FrontendCli
from lib.frontend_gtk import FrontendGtk
from lib.printing import printerr


def test_frontend_user_confirm(frontend: Frontend):
    choice = frontend.get_user_confirmation("Confirm?")
    printerr("Your choice: "+str(choice))


def test_frontend_get_tags(frontend: Frontend, tags_choice: List[str]):
    choice = frontend.get_tags(tags_choice)
    printerr("Your choice:")
    for t in choice:
        printerr(t)


printerr("Testing batch frontend")
test_frontend_get_tags(FrontendBatch(), ["foo", "bar", "foo bar"])
test_frontend_user_confirm(FrontendBatch())

printerr("Testing CLI frontend")
test_frontend_get_tags(FrontendCli(), ["foo", "bar", "foo bar", "äöl"])
test_frontend_user_confirm(FrontendCli())

printerr("Testing GTK frontend")
test_frontend_get_tags(FrontendGtk(), ["foo", "bar", "foo bar", "äöl"])
test_frontend_user_confirm(FrontendGtk())

