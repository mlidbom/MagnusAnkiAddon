from __future__ import annotations

import re

from sysutils.collections.linq.l_iterable import LList

newline = "\n"
invisible_space = "​"
full_width_space = "　"

def pad_to_length(value: str, target_length: int, space_scaling: float = 1.0) -> str:
    padding = max(0, target_length - len(value))
    return value + " " * int(padding * space_scaling)

_commaSeparatedPattern = f"""[{''.join(map(re.escape, (",", "、")))}]"""
_commaSeparatedCompiled = re.compile(_commaSeparatedPattern)
def extract_comma_separated_values(string: str) -> LList[str]:
    return LList(item for item in (item.strip() for item in _commaSeparatedCompiled.split(string.strip())) if item)

_html_bracket_pattern = re.compile('<.*?>|\[.*?\]') # noqa  # pyright: ignore[reportInvalidStringEscapeSequence] don't know what's going on here but it has been working for ages
def strip_html_and_bracket_markup(string: str) -> str:
    return _html_bracket_pattern.sub("", string)

def replace_html_and_bracket_markup_with(string: str, replacement:str) -> str:
    return _html_bracket_pattern.sub(replacement, string)

_html_pattern = re.compile("<.*?>|&nbsp;")
def strip_html_markup(string: str) -> str:
    return _html_pattern.sub("", string)

html_bracket_noise_pattern = re.compile('<.*?>|\[.*?\]|[〜]') # noqa  # pyright: ignore[reportInvalidStringEscapeSequence] don't know what's going on here but it has been working for ages
def strip_html_and_bracket_markup_and_noise_characters(string: str) -> str:
    return html_bracket_noise_pattern.sub("", string)

def strip_brackets(string:str) -> str:
    return string.replace("[","").replace("]","")

_first_number_pattern = re.compile(r"\d+")
def first_number(string:str) -> int:
    match = _first_number_pattern.search(string)
    assert match
    return int(match.group())

def replace_word(word:str, replacement:str, text:str) -> str:
    return re.sub(rf"\b{re.escape(word)}\b", replacement, text)