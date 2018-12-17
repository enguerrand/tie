import os

from pytag import cli

TAGS_DIR_NAME = "tags"


class Index:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.tags_dir = os.path.join(self.root_dir, TAGS_DIR_NAME)
        self._create_if_absent()

    def _create_if_absent(self):
        cli.run_cmd(["mkdir", "-p", self.tags_dir])

