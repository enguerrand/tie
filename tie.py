#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from lib import config, tie_main
from lib import frontend_factory as ff
from lib.exif_editor import ExifEditor
from lib.exit_codes import EXIT_CODE_PARSE_ERROR, EXIT_CODE_FILE_NOT_FOUND
from lib.index import Index
from lib.options_parser import RunOptions, ParseError, USAGE_STRING, Action
from lib.printing import printerr
from lib.tie_core import TieCoreImpl


def setup_sys_path():
    own_path = sys.argv[0]
    basedir = os.path.dirname(own_path)
    sys.path.append(basedir)


def print_usage():
    print(USAGE_STRING)


def main(*args):
    try:
        setup_sys_path()

        configuration = config.load_user_config()

        run_options = RunOptions(list(args[1:]))

        frontend_type = run_options.frontend
        front_end = ff.from_type(frontend_type)

        index_root_dir = configuration.index_path
        exif = ExifEditor(configuration.exif_field_name)
        index = Index(index_root_dir, exif)

        core = TieCoreImpl(exif, index)

        if run_options.action == Action.help:
            print_usage()
        else:
            tie_main.run(core, run_options, front_end)

    except ParseError as parse_error:
        printerr("Error: " + parse_error.msg)
        print_usage()
        sys.exit(EXIT_CODE_PARSE_ERROR)
    except FileNotFoundError:
        # No need to print it. this is already done by subprocess
        sys.exit(EXIT_CODE_FILE_NOT_FOUND)


main(*sys.argv)