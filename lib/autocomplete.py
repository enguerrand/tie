# -*- coding: utf-8 -*-
from typing import List


def auto_complete(user_input: str, available_options: List[str]) -> str:
    alternatives = get_auto_complete_alternatives(user_input, available_options)
    if len(alternatives) == 0:
        return user_input
    result = extract_common_prefix(alternatives)
    return result


def get_auto_complete_alternatives(user_input: str, available_options: List[str]) -> List[str]:
    alternatives = list()
    for option in available_options:
        if option == user_input:
            return list()
        elif option.startswith(user_input):
            alternatives.append(option)
    return alternatives


def extract_common_prefix(options: List[str]) -> str:
    if len(options) == 0:
        return ""
    matching_substring = ""
    while True:
        current_index = len(matching_substring)
        current_character = None
        for o in options:
            if len(o) == current_index:
                return matching_substring
            elif current_character is None:
                current_character = o[current_index]
            elif current_character != o[current_index]:
                return matching_substring
        matching_substring += current_character
