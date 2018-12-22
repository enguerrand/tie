#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from lib import config, tie_main
from lib import frontend_factory as ff
from lib.exif_editor import ExifEditor
from lib.index import Index
from lib.meta_data import InvalidMetaDataError
from lib.options_parser import RunOptions, ParseError
from lib.printing import printerr
from lib.tie_core import TieCoreImpl


def setup_sys_path():
    own_path = sys.argv[0]
    basedir = os.path.dirname(own_path)
    sys.path.append(basedir)


def main(*args):
    try:
        setup_sys_path()

        run_options = RunOptions(list(args[1:]))

        frontend_type = run_options.frontend
        front_end = ff.from_type(frontend_type)

        index_root_dir = config.get_or_create_default_config_dir() # TODO: Support customizing config dir
        exif = ExifEditor() # TODO: Support specifying custom exif field name
        index = Index(index_root_dir, exif)
        core = TieCoreImpl(exif, index)

        tie_main.run(core, run_options, front_end)

    except ParseError as parse_error:
        printerr("Error: " + parse_error.msg)
        sys.exit(1)
    except InvalidMetaDataError as meta_data_error:
        # TODO: Use frontend to ask for confirmation to clear file
        printerr("Error: Cannot edit file - " + meta_data_error.msg)
        printerr("Run \"tie --clear\" on it to clean it")
        sys.exit(2)
    except FileNotFoundError:
        # No need to print it. this is already done by subprocess
        sys.exit(3)


main(*sys.argv)
