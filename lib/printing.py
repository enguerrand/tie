import csv
import sys
from typing import List


def printstd(msg: str):
    print(msg)


def printerr(msg: str):
    print(msg, file=sys.stderr)


def print_out_list(out: List[str]):
    writer = csv.writer(sys.stdout, delimiter=" ", quotechar="'", lineterminator="")
    writer.writerow(out)
