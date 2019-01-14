import os

from lib import cli


def ln(destination: str, link_name: str):
    # "os.symlink(source, destination)" does not provide a race-free way to force the symlink creation
    cli.run_cmd(["ln", "-sf", destination, link_name])


def readlink(link: str) -> str:
    return os.readlink(link)


def is_broken(path: str):
    if not os.path.islink(path):
        return True
    return not os.path.exists(readlink(path))


def rm(link: str) -> str:
    """
    :raises NotASymlinkError when trying to remove a file that is not a symlink
    """
    path = _remove_trailing_slashes(link)
    if not os.path.islink(path):
        raise NotASymlinkError("The file "+link+" is not a symlink!")

    os.remove(path)


def _remove_trailing_slashes(path: str) -> str:
    return path.rstrip("/")


class NotASymlinkError(Exception):
    pass
