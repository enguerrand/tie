from lib.abstract_frontend import Frontend
from lib.options_parser import RunOptions, Action

from lib.printing import print_out_list
from lib.query import Query
from lib.tie_core import TieCore


def run(core: TieCore, run_options: RunOptions, front_end: Frontend):
    if run_options.needs_tags():
        run_options.tags = front_end.get_tags()
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
