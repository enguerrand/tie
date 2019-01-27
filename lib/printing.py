# -*- coding: utf-8 -*-
import os
import sys
from typing import List


def printstd(msg: str):
    print(msg)


def printerr(msg: str):
    print(msg, file=sys.stderr)


def print_out_list(out: List[str]):
    for i in out:
        printstd(i)


def redirect_stdout() -> int:
    backup_fd = os.dup(1)
    os.dup2(2, 1)
    return backup_fd


def revert_stdout(backup_fd: int):
    os.dup2(backup_fd, 1)
    os.close(backup_fd)

