from typing import List

from tie.abstract_frontend import Frontend


class FrontendCli(Frontend):
    def get_tags(self) -> List[str]:
        # TODO: Implement interactive user input
        return ["foobar"]
