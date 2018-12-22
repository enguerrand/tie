import subprocess
from typing import List


def run_cmd(words: List[str]) -> List[str]:
    cp = subprocess.run(words, stdout=subprocess.PIPE)
    cp.check_returncode()
    return cp.stdout.decode("utf-8").split("\n")
