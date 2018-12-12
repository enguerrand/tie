import subprocess


class Cli:

    def run_cmd(self, words):
        print("Running command: "+" ".join(words))
        cp = subprocess.run(words, stdout=subprocess.PIPE)
        cp.check_returncode()
        return cp.stdout.decode("utf-8").split("\n")
