# -*- coding: utf-8 -*-
import subprocess
from subprocess import CalledProcessError
from typing import List


def run_cmd(words: List[str], suppress_error_code=None) -> List[str]:
    cp = subprocess.run(words, stdout=subprocess.PIPE)
    try:
        cp.check_returncode()
    except CalledProcessError as e:
        if e.returncode != suppress_error_code:
            raise e
    return cp.stdout.decode("utf-8").split("\n")
