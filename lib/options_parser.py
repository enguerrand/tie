from enum import Enum
from typing import List

from lib.query import MatchType


class ParsingStage(Enum):
    action = 1
    tags = 2
    files = 3


class Action(Enum):
    query = 1
    list = 2
    tag = 3
    untag = 4
    clear = 5
    index = 6


_short_actions = {
    'q': Action.query,
    'l': Action.list,
    't': Action.tag,
    'u': Action.untag,
    'c': Action.clear,
    'i': Action.index,
}


class FrontendType(Enum):
    batch = 1
    cli = 2
    gtk = 3


class Option:
    def __init__(self, short: str, long: str):
        self.short = short
        self.long = long

    def matches(self, arg: str) -> bool:
        return arg == self.short or arg == self.long


class ParseError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class RunOptions:
    def __init__(self, args: List[str]):
        """
        :raises ParseError if the provided args are invalid
        """
        self.action: Action = None
        self.tags: List[str] = []
        self.files: List[str] = []
        self.match_type: MatchType = MatchType.all
        self.frontend: FrontendType = None
        self._parse(args)
        self._check_action_type()
        self._check_files_count()
        if self.frontend is None:
            self.frontend = FrontendType.cli

    def _parse(self, args: List[str]):
        parsing_stage = ParsingStage.action

        while len(args) > 0:
            arg = args.pop(0)
            if is_option(arg):
                if Option("-f", "--files").matches(arg):
                    parsing_stage = ParsingStage.files
                elif Option("-F", "--frontend").matches(arg):
                    if len(args) == 0:
                        raise ParseError("Argument missing for option --frontend!")
                    self.frontend = FrontendType[args.pop(0)]
                elif Option("-m", "--match-type").matches(arg):
                    if len(args) == 0:
                        raise ParseError("Argument missing for option --match-type!")
                    self.match_type = MatchType[args.pop(0)]
                else:
                    raise ParseError("Unknown option "+arg)
            elif parsing_stage == ParsingStage.action:
                if arg in _short_actions:
                    self.action = _short_actions[arg]
                else:
                    try:
                        self.action = Action[arg]
                    except KeyError:
                        raise ParseError("Invalid action type: "+arg)
                parsing_stage = ParsingStage.tags
            elif parsing_stage == ParsingStage.tags:
                self.tags.append(arg)
            elif parsing_stage == ParsingStage.files:
                self.files.append(arg)

    def needs_tags(self) -> bool:
        if len(self.tags) > 0:
            return False
        return self.action in [Action.query, Action.tag, Action.untag]

    def _check_action_type(self):
        if self.action is None:
            raise ParseError("Action type must be specified!")

    def _check_files_count(self):
        actual_file_count = len(self.files)

        if self.action in [Action.tag, Action.untag, Action.clear, Action.index] and actual_file_count < 1:
            raise ParseError("Unexpected files count " + str(actual_file_count) +
                             " (expected 1 or more) for action type \"" + self.action.name + "\"")
        elif self.action == Action.list and actual_file_count != 1:
            raise ParseError("Unexpected files count " + str(actual_file_count) +
                             " (expected 1) for action type \"" + self.action.name + "\"")
        elif self.action == Action.query and actual_file_count > 0:
            raise ParseError("Unexpected files count " + str(actual_file_count) +
                             " (expected 0) for action type \"" + self.action.name + "\"")


def is_option(arg: str):
    return arg.startswith("-")


