from typing import List

from lib.abstract_frontend import Frontend
from lib.frontend_batch import FrontendBatch
from lib.frontend_cli import FrontendCli


def test_frontend_get_tags(frontend: Frontend, tags_choice: List[str]):
    choice = frontend.get_tags(tags_choice)
    print("Your choice:")
    for t in choice:
        print(t)


print("Testing batch frontend")
test_frontend_get_tags(FrontendBatch(), ["foo", "bar", "foo bar"])

print("Testing CLI frontend")
test_frontend_get_tags(FrontendCli(), ["foo", "bar", "foo bar", "äöl"])
