# -*- coding: utf-8 -*-
from enum import Enum
from typing import List

from lib.query import MatchType

USAGE_STRING = """Usage: tie.py action [tags] [options]

Tie is an acronym for "tags in exif-data". 
It "ties" tags to image files using exif data fields while also maintaining a symlink-based index of tagged files for 
querying purposes.


ACTIONS:
    help:   print this help
    query:  query for files with specified tags
    list:   list all tags present on the specified files
    tag:    add specified tag to specified file(s)
    untag:  remove specified tag from specified file(s)
    clear:  clear all tags from specified file(s)
    index:  update the index for the specied file(s)

All actions may be called with their full name or just their initial character.
In other words, the following two commands are equivalent:

    tie.py help
    tie.py h


OPTIONS:
    -f, --files file_1 [file_2 ... ]
        Specifies the files to apply the chosen action to.
        If this option is omitted and the specified action requires a specification of target files, the last 
        argument will be treated as a file argument. 
        In this case no other options may follow the file specification.

    -F, --frontend batch|yes|cli|gtk
        Chooses the frontend. The default is cli. Possible choices:
            batch: Non-interactive mode suitable for scripts. The answer to yes/no questions is aways "no".
            yes:   Behaves as the batch frontend but always answers yes/no questions with "yes".
            cli:   Interactive command line interface.
            gtk:   Graphical user interface. Requires a running X session and gtk.
        
    -m, --match-type all|any
        Only applicable for the query action. Specifies whether to query for files that contain all or any of the
        specified tags, respectively.


Depending on the chosen action, tags must be specified. All non-option-arguments that are provided after the action 
argument and before the files specification are interpreted as tags.


CONFIGURATION:
The default configuration file path is $HOME/.tie.ini
This location can be overridden by setting the environment variable TIE_CONFIG_PATH to the desired path.
The syntax follows the .ini file format. See more detailed description and example below.

The following settings can be configured:
    
    exif_field:
        The exif field that is used to store and retrieve tag data. Defaults to "Exif.Photo.UserComment"
        
    index_path:
        The path to the directory where the symlink-based index is stored. Defaults to $HOME/.tie/


EXAMPLES:
    Querying:
        tie query tag
        
    Querying for tags with white spaces:
        tie query 'tag 1' 'tag 2'

    Querying with short form for action:
        tie q tag
    
    Interactive querying in default (cli) frontend:
        tie query

    Interactive querying in gtk frontend:
        tie query --frontend gtk
    
    Listing tags
        tie list -f /path/to/file1 [/path/to/file2..]
    
    Tagging one file
        tie tag tag1 tag2 /path/to/file1
        
    Tagging multiple files with the same tags
        tie tag tag1 tag2 --files /path/to/file1 [/path/to/file2..]
    
    Untagging
        tie untag tag1 tag2 --files /path/to/file1 [/path/to/file2..]
    
    Clearing all tags
        tie clear --files /path/to/file1 [/path/to/file2..]
    
    Updating the index
        tie index --files /path/to/file1 [/path/to/file2..]
        
    Example configuration file with current default values:
        [GENERAL]
        index_path = /home/foo/.tie/
        [EXIV2]
        exif_field = Exif.Photo.UserComment
        charset = UTF-8
        quiet = yes
        keep_time_stamps = yes
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
                    self.frontend = _parse_frontend_type(args)
                elif Option("-m", "--match-type").matches(arg):
                    self.match_type = _parse_match_type(args)
                else:
                    raise ParseError("Unknown option "+arg)
            elif parsing_stage == ParsingStage.action:
                self.action = _parse_action(arg)
                if self.needs_tags():
                    parsing_stage = ParsingStage.tags
                else:
                    parsing_stage = ParsingStage.files
            elif parsing_stage == ParsingStage.tags:
                self.tags.append(arg)
            elif parsing_stage == ParsingStage.files:
                self.files.append(arg)

    def needs_tags(self) -> bool:
        if len(self.tags) > 0:
            return False
        return self.action in [Action.query, Action.tag, Action.untag]

    def allows_tag_creation(self) -> bool:
        return self.action == Action.tag

    def _check_action_type(self):
        if self.action is None:
            raise ParseError("Action type must be specified!")

    def _check_files_count(self):
        actual_file_count = len(self.files)

        if self.action in [Action.list, Action.tag, Action.untag, Action.clear, Action.index] and actual_file_count < 1:
            raise ParseError("Unexpected files count " + str(actual_file_count) +
                             " (expected 1 or more) for action type \"" + self.action.name + "\"")
        elif self.action == Action.query and actual_file_count > 0:
            raise ParseError("Unexpected files count " + str(actual_file_count) +
                             " (expected 0) for action type \"" + self.action.name + "\"")


def _parse_match_type(args):
    if len(args) == 0:
        raise ParseError("Argument missing for option --match-type!")
    return MatchType[args.pop(0)]


def _parse_frontend_type(args):
    if len(args) == 0:
        raise ParseError("Argument missing for option --frontend!")
    try:
        return FrontendType[args.pop(0)]
    except KeyError:
        raise ParseError("Invalid frontend type " + args.pop(0))


def _parse_action(action_name):
    if action_name in _short_actions:
        return _short_actions[action_name]
    else:
        try:
            return Action[action_name]
        except KeyError:
            raise ParseError("Invalid action type: " + action_name)


def _is_option(arg: str):
    return arg.startswith("-")


def _requires_files(action):
    return action in [Action.list, Action.tag, Action.untag, Action.clear, Action.index]


