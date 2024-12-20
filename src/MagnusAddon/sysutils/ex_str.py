import re

newline = "\n"
full_width_space = "　"

def pad_to_length(value: str, target_length: int, space_scaling: float = 1.0) -> str:
    padding = max(0, target_length - len(value))
    return value + " " * int(padding * space_scaling)

def pad_to_length_ui_font(text: str, length: int) -> str:
    return pad_to_length(text, length, 1.5)

def extract_characters(string: str) -> list[str]:
    return [char for char in string if not char.isspace()]

_commaSeparatedPattern = f"""[{''.join(map(re.escape, (",", "、")))}]"""
_commaSeparatedCompiled = re.compile(_commaSeparatedPattern)
def extract_comma_separated_values(string: str) -> list[str]:
    return [item for item in (item.strip() for item in _commaSeparatedCompiled.split(string.strip())) if item]

def extract_newline_separated_values(string: str) -> list[str]:
    return [item for item in string.split(newline) if item]

_html_bracket_pattern = re.compile('<.*?>|\[.*?\]') # noqa
def strip_html_and_bracket_markup(string: str) -> str:
    return _html_bracket_pattern.sub('', string)

_html_pattern = re.compile('<.*?>|&nbsp;')
def strip_html_markup(string: str) -> str:
    return _html_pattern.sub('', string)

html_bracket_noise_pattern = re.compile('<.*?>|\[.*?\]|[〜]') # noqa
def strip_html_and_bracket_markup_and_noise_characters(string: str) -> str:
    return html_bracket_noise_pattern.sub('', string)

_first_number_pattern = re.compile(r'\d+')
def first_number(string:str) -> int:
    match = _first_number_pattern.search(string)
    assert match
    return int(match.group())

def replace_word(word:str, replacement:str, text:str) -> str:
    return re.sub(rf'\b{re.escape(word)}\b', replacement, text)