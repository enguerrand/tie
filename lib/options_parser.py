from enum import Enum
from typing import List

from lib.query import MatchType

USAGE_STRING = """
    usage: tie.py action [options] [tags] [files]
    
    
    ACTIONS:
        help:   print this help
        query:  query for files with specified tags
        list:   list tags of specified file(s)
        tag:    add specified tag to specified file(s)
        untag:  remove specified tag from specified file(s)
        clear:  clear all tags from specified file(s)
        index:  update the index for the specied file(s)
    
    All actions may be called with their full name or just their initial character.
    In other words, the following to commands are equivalent:
    
        tie.py help
        tie.py h
    
    
    OPTIONS:
        -f, --files
            All subsequent non-option-arguments will be interpreted as file specifications.
            If this option is omitted and the specified action requires a file specification, the
            last non-option argument will be treated as the file specification.
                        
        -F, --frontend batch|yes|cli|gtk
            Chooses the frontend. The default is cli (command line interface).
            The batch frontend is non-interactive mode suitable for scripts. The answer to yes/no questions is aways no.
            The yes frontend behaves as the batch frontend but always answers yes/no questions with yes..
            The gtk interface requires a running X session and gtk.
            
        -m, --match-type all|any
            Only applicable for the query action. Specifies whether to query for file that contain all or any of the
            specified tags, respectively.
    
    
    Depending on the chosen action, tags must be specified. All non-option-arguments that are provided after the
    action argument and before the files specification are interpreted as tags.
    
    
    EXAMPLES:
        Querying:
            tie query 'tag 1' tag2

        Querying with short form for action:
            tie q 'tag 1' tag2
        
        Interactive querying:
            tie query --frontend gtk
        
        Listing tags
            tie list /path/to/file
        
        Tagging one file
            tie tag 'tag 1' tag2/path/to/file1
            
        Tagging multiple files with the same tags
            tie tag 'tag 1' tag2 --files /path/to/file1 [/path/to/file2..]
        
        Untagging
            tie untag 'tag 1' tag2 --files /path/to/file1 [/path/to/file2..]
        
        Clearing all tags
            tie clear --files /path/to/file1 [/path/to/file2..]
        
        Updating the index
            tie index -f|--files /path/to/file1 [/path/to/file2..]
        
    
"""


class ParsingStage(Enum):
    action = 1
    tags = 2
    files = 3


class Action(Enum):
    help = 1
    query = 2
    list = 3
    tag = 4
    untag = 5
    clear = 6
    index = 7


_short_actions = {
    'h': Action.help,
    'q': Action.query,
    'l': Action.list,
    't': Action.tag,
    'u': Action.untag,
    'c': Action.clear,
    'i': Action.index,
}


class FrontendType(Enum):
    batch = 1
    yes = 2
    cli = 3
    gtk = 4


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

            if parsing_stage == ParsingStage.tags and _requires_files(self.action) and len(args) == 0:
                parsing_stage = ParsingStage.files

            if _is_option(arg):
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


def _is_option(arg: str):
    return arg.startswith("-")


def _requires_files(action):
    return action in [Action.list, Action.tag, Action.untag, Action.clear, Action.index]


