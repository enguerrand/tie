from enum import Enum
from typing import List

from tie.query import MatchType


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
        if self.action is None:
            raise ParseError("Action type must be specified!")
        if self._needs_files():
            raise ParseError("Need files spec for action type "+self.action.name)
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
                    self.frontend = FrontendType[args.pop(0)]
                elif Option("-m", "--match-type").matches(arg):
                    self.match_type = MatchType[args.pop(0)]
                else:
                    raise ParseError("Unknown option "+arg)
            elif parsing_stage == ParsingStage.action:
                try:
                    self.action = Action[arg]
                except KeyError:
                    raise ParseError("Inbalid action type: "+arg)
                parsing_stage = ParsingStage.tags
            elif parsing_stage == ParsingStage.tags:
                self.tags.append(arg)
            elif parsing_stage == ParsingStage.files:
                self.files.append(arg)

    def needs_tags(self) -> bool:
        if len(self.tags) > 0:
            return False
        return self.action in [Action.query, Action.tag, Action.untag]

    def _needs_files(self) -> bool:
        if len(self.files) > 0:
            return False
        return self.action in [Action.list, Action.tag, Action.untag, Action.clear, Action.index]


def is_option(arg: str):
    return arg.startswith("-")


