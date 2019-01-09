import sys

from lib.abstract_frontend import Frontend
from lib.exit_codes import EXIT_CODE_INVALID_META_DATA, EXIT_CODE_PARSE_ERROR
from lib.meta_data import InvalidMetaDataError
from lib.options_parser import RunOptions, Action, ParseError

from lib.printing import print_out_list, printerr
from lib.query import Query
from lib.tie_core import TieCore


def run(core: TieCore, run_options: RunOptions, front_end: Frontend):
    _check_tags(core, front_end, run_options)
    try:
        _run_action(core, run_options)
    except InvalidMetaDataError as meta_data_error:
        # TODO: Use frontend to ask for confirmation to clear file
        printerr("Error: Cannot edit file - " + meta_data_error.msg)
        printerr("Run \"tie --clear\" on it to clean it")
        sys.exit(EXIT_CODE_INVALID_META_DATA)


def _check_tags(core, front_end, run_options):
    if run_options.needs_tags():
        run_options.tags = front_end.get_tags(core.list_all_tags())
        if len(run_options.tags) == 0:
            raise ParseError("Cannot execute command \"" + run_options.action.name + "\" with empty tags list")


def _run_action(core, run_options):
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
                raise Exception("Unexpected action type " + action.name)
            core.update_index(file)
