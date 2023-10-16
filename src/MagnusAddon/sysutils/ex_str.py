import re


newline = "\n"
full_width_space = "　"

def pad_to_length(value: str, target_length: int, space_scaling:float = 1.0) -> str:
    padding = max(0, target_length - len(value))
    return value + " " * int(padding * space_scaling)

def pad_to_length_ui_font(text:str, length: int) -> str:
    return pad_to_length(text, length, 1.5)

def extract_characters(string: str) -> list[str]:
    return [char for char in string if not char.isspace()]

def extract_token_separated_values(string: str, token: str) -> list[str]:
    return [item for item in (item.strip() for item in string.strip().split(token)) if item]

def extract_comma_separated_values(string: str) -> list[str]:
    return extract_token_separated_values(string, ",")

def extract_newline_separated_values(string: str) -> list[str]:
    return extract_token_separated_values(string, newline)


def strip_html_and_bracket_markup(string: str) -> str:
    return re.sub('<.*?>|\[.*?\]', '', string) # noqa

def strip_html_markup(string: str) -> str:
    return re.sub('<.*?>', '', string) # noqa


def strip_html_and_bracket_markup_and_noise_characters(string: str) -> str:
    return re.sub('<.*?>|\[.*?\]|[〜]', '', string)  # noqa

def remove_duplicates_characters(input_str: str) -> str:
    seen = set()
    output_str = ""
    for char in input_str:
        if char not in seen:
            seen.add(char)
            output_str += char
    return output_str