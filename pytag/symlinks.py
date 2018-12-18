import os

from pytag import cli


def ln(destination: str, link_name: str):
    # "os.symlink(source, destination)" does not provide a way to force the symlink creation
    cli.run_cmd(["ln", "-sf", destination, link_name])


def readlink(link: str) -> str:
    return os.readlink(link)


def rm(link: str) -> str:
    """
        Raises: NotASymlinkError when trying to remove a file that is not a symlink
    """
    path = _remove_trailing_slashes(link)
    if not os.path.islink(path):
        raise NotASymlinkError("The file "+link+" is not a symlink!")

    os.remove(path)


def _remove_trailing_slashes(path: str) -> str:
    return path.rstrip("/")


class NotASymlinkError(Exception):
    pass
