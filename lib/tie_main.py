from typing import List

from lib.abstract_frontend import Frontend
from lib.meta_data import InvalidMetaDataError
from lib.options_parser import RunOptions, Action, ParseError

from lib.printing import print_out_list, printerr
from lib.query import Query
from lib.tie_core import TieCore


def run(core: TieCore, run_options: RunOptions, front_end: Frontend):
    """
    :raises: InvalidMetaDataError if a file still has invalid metadata after an attempt to clear invalid data
             CalledProcessError if the exiv2 command terminated abnormally
    """
    _check_tags(core, front_end, run_options)
    _run_action(core, run_options, front_end)


def _check_tags(core: TieCore, front_end: Frontend, run_options: RunOptions):
    if run_options.needs_tags():
        if run_options.action == Action.untag:
            _check_tags_untag(core, front_end, run_options)
        else:
            run_options.tags = front_end.get_tags(core.list_all_tags(), run_options.allows_tag_creation())
        if len(run_options.tags) == 0:
            raise ParseError("Cannot execute command \"" + run_options.action.name + "\" with empty tags list")


def _check_tags_untag(core, front_end: Frontend, run_options: RunOptions):
    present_tags = core.list(run_options.files)
    if len(present_tags) == 0:
        raise ParseError("Cannot execute command \"" + run_options.action.name + "\": No tags present on selected files")
    run_options.tags = front_end.get_tags(sorted(list(present_tags)), False)


def _run_action(core: TieCore, run_options: RunOptions, frontend: Frontend):
    action = run_options.action
    if action == Action.query:
        _query(core, run_options.tags, run_options.match_type)
    elif action == Action.list:
        _list(core, run_options.files, frontend)
    else:
        for file in run_options.files:
            try:
                _process_file(core, file, run_options)
            except InvalidMetaDataError as meta_data_error:
                _handle_invalid_meta_data(core, file, frontend, meta_data_error, run_options)


def _query(core, tags, match_type):
    query = Query(tags, match_type)
    out = core.query(query)
    print_out_list(out)


def _list(core, files: List[str], frontend: Frontend):
    out = core.list(files)
    frontend.list_tags(files, out)


def _process_file(core, file, run_options):
    action = run_options.action
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
        raise Exception("Unexpected action type " + action.name)
    core.update_index(file)


def _handle_invalid_meta_data(core, file, frontend, meta_data_error, run_options):
    clear = frontend.get_user_confirmation(
        "Error: Cannot read metadata from file " + file + " - " + meta_data_error.msg + "\n"
                                                                          "Clear present meta data now?")
    if clear:
        core.clear(file)
        # Hopefully the file is clean now. If whatever reason it isn't, this call will raise an
        # InvalidMetaDataError again. If it does, let it bubble up.
        _process_file(core, file, run_options)
    else:
        printerr("Ignoring unreadable file " + file)
