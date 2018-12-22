#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from lib import frontend_factory as ff
from lib import config
from lib.exif_editor import ExifEditor
from lib.index import Index
from lib.meta_data import InvalidMetaDataError
from lib.options_parser import RunOptions, Action, ParseError
from lib.printing import printerr, print_out_list
from lib.query import Query
from lib.tie_core import TieCoreImpl, TieCore


def _fetch_tags(run_options: RunOptions):
    frontend_type = run_options.frontend
    front_end = ff.from_type(frontend_type)
    run_options.tags = front_end.get_tags()


def run(core: TieCore, run_options: RunOptions):
    action = run_options.action
    if action == Action.query:
        out = core.query(Query(run_options.tags, run_options.match_type))
        print_out_list(out)
    elif action == Action.list:
        out = core.list(run_options.files[0])
        print_out_list(out)
    else:
        for file in run_options.files:
            if action == Action.tag:
                core.tag(file, run_options.tags)
            elif action == Action.untag:
                core.untag(file, run_options.tags)
            elif action == Action.clear:
                core.clear(file)
            elif action == Action.index:
                # This happens below
                pass
            else:
                raise Exception("Unexpected action type "+action.name)
            core.update_index(file)


def setup_sys_path():
    own_path = sys.argv[0]
    basedir = os.path.dirname(own_path)
    sys.path.append(basedir)


def main(*args):
    try:
        setup_sys_path()

        run_options = RunOptions(list(args[1:]))
        if run_options.needs_tags():
            _fetch_tags(run_options)

        index_root_dir = config.get_or_create_default_config_dir() # TODO: Support customizing config dir
        exif = ExifEditor() # TODO: Support specifying custom exif field name
        index = Index(index_root_dir, exif)
        core = TieCoreImpl(exif, index)
        run(core, run_options)

    except ParseError as parse_error:
        printerr("Error: " + parse_error.msg)
    except InvalidMetaDataError as meta_data_error:
        printerr("Error: Cannot edit file - Invalid meta data present. Run \"tie --clear\" on it to clean it")


main(*sys.argv)
