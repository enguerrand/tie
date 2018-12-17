import os

from pytag import cli


def ln(destination: str, source: str):
    # "os.symlink(source, destination)" does not provide a way to force the symlink creation
    cli.run_cmd(["ln", "-sf", source, destination])


def readlink(link: str) -> str:
    return os.readlink(link)


def rm(link: str) -> str:
    path = _remove_trailing_slashes(link)
    if not os.path.islink(path):
        raise TypeError("The file "+link+" is not a symlink!")

    os.remove(path)


def _remove_trailing_slashes(path: str) -> str:
    return path.rstrip("/")
